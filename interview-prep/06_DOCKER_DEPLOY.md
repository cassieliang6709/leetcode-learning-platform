# Docker 部署方案

## 架构（Docker Compose 本地演示）

```
docker-compose.yml
├── postgres (pgvector/pgvector:pg16)   ← port 5432
│     └── pgvector extension enabled
├── redis (redis:7-alpine)              ← port 6379
│     └── rate limit 计数存储
├── piston (ghcr.io/engineer-man/piston) ← port 2000
│     ├── privileged: true（需要管理 Docker containers）
│     ├── python 3.10, javascript 18, java 15, cpp, go, rust
│     └── 每次执行：独立容器 + 5秒超时 + 128MB 内存
└── backend (自建 Dockerfile)          ← port 8000
      ├── PISTON_URL=http://piston:2000/api/v2
      ├── DATABASE_URL=...@postgres:5432/...
      └── REDIS_URL=redis://redis:6379
```

## 关键设计决策

### 为什么用 self-hosted Piston 而不是公共 API？
- 面试要求代码对得上简历（"Docker containers to isolate"）
- 自建实例：100% 控制资源限制，不依赖外部服务
- 生产场景：公共 Piston 可能有并发限制、延迟不稳定
- 本地演示：完全离线运行

### Piston 的隔离机制
- 每个代码提交 → Piston 创建一个新的 Docker 容器
- 容器内：`--network=none`（无网络访问）
- 内存限制：`run_memory_limit: 128MB`
- CPU 超时：`run_timeout: 5000ms`
- 执行完毕 → 容器立即销毁
- Cgroup 由 Docker 底层管理（`--memory` flag → `/sys/fs/cgroup/memory.max`）

### pgvector 集成
- 使用 `pgvector/pgvector:pg16` 官方镜像（内置 pgvector 扩展）
- `scripts/init_db.sql` 在容器首次启动时自动执行：`CREATE EXTENSION IF NOT EXISTS vector`
- 不需要手动配置

### PISTON_URL 环境变量
```python
# code_executor.py
BASE_URL: str = os.getenv("PISTON_URL", "https://emkc.org/api/v2/piston")
```
- Docker Compose：`PISTON_URL=http://piston:2000/api/v2`（自建）
- Railway/Cloud：不设置 → 自动 fallback 到公共 API
- 无缝切换，不需要改代码

## 面试问题准备

**Q: privileged: true 不是安全风险吗？**
A: Piston 需要 privileged 权限在内部创建 Docker 容器（Docker-in-Docker）。这个容器本身在专用网络里，不对外暴露除 2000 端口以外的任何接口。用户提交的代码运行在 Piston 创建的子容器里，与宿主机隔离了两层（Docker → Piston → user container）。生产环境可以用 rootless Docker 或 gVisor 进一步降低风险。

**Q: Docker Compose 能上生产吗？**
A: 可以，单机部署 docker compose up -d 完全够用。如果需要高可用或自动扩缩容，会迁移到 Kubernetes 或 Railway + 独立 Piston 实例。

**Q: Piston 语言运行时是怎么安装的？**
A: Piston 有个 package manager，首次启动后调用 `POST /api/v2/packages` 安装每个语言的 runtime。我写了 `scripts/setup_piston.sh` 自动安装所有需要的语言。安装的 runtime 持久化在 `piston_data` volume 里，重启不丢失。

## 部署到 Railway（生产）

Railway 不支持 Docker-in-Docker（无法跑 self-hosted Piston），所以：
- Backend 部署到 Railway（普通 Docker 部署）
- PostgreSQL 用 Railway 提供的 managed Postgres + 手动 enable pgvector
- Redis 用 Railway 提供的 managed Redis
- 代码执行：`PISTON_URL` 不设置 → fallback 到公共 Piston API

```
Railway 部署时设置的环境变量：
DATABASE_URL=<railway postgres url>
REDIS_URL=<railway redis url>
SECRET_KEY=<random secret>
SILICONFLOW_API_KEY=<your key>
# PISTON_URL 不设置 → 使用公共 API
```
