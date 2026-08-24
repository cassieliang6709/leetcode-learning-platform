import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './LandingPage.css'

const highlights = [
  {
    title: 'Learn the patterns',
    description:
      'Follow a structured roadmap across arrays, sliding window, trees, graphs, dynamic programming, and other core interview topics.',
  },
  {
    title: 'Practice in one workspace',
    description:
      'Solve curated LeetCode-style problems with a built-in editor, starter code, test runs, and full submissions.',
  },
  {
    title: 'Get grounded AI guidance',
    description:
      'Receive hints and feedback tied to the project knowledge base, so the AI explains concepts instead of guessing.',
  },
]

const capabilities = [
  '89 coding problems for interview practice',
  '13 topic roadmap with learning content',
  'Three levels of AI hints based on your code',
  'Code execution for Python, JavaScript, Java, and C++',
  'Semantic search to find similar problems quickly',
  'Submission history and progress-aware feedback',
]

const steps = [
  {
    number: '01',
    title: 'Study a topic',
    description:
      'Open the roadmap, review the core idea, and understand the pattern before jumping into implementation.',
  },
  {
    number: '02',
    title: 'Write and test code',
    description:
      'Use the editor to run examples, submit solutions, and see where your implementation breaks.',
  },
  {
    number: '03',
    title: 'Improve with AI help',
    description:
      'Ask for hints, failure analysis, or optimization advice that references the platform curriculum.',
  },
]

const LandingPage = () => {
  const { isAuthenticated } = useAuth()

  return (
    <div className="landing-page">
      <section className="landing-hero">
        <div className="landing-hero-copy">
          <p className="landing-eyebrow">AlgoMentor</p>
          <h1>One place to learn algorithms, solve problems, and get AI-guided interview practice.</h1>
          <p className="landing-intro">
            AlgoMentor is a full-stack coding interview prep platform. It combines a learning roadmap,
            LeetCode-style practice, isolated code execution, and retrieval-augmented AI feedback into a
            single product.
          </p>
          <div className="landing-actions">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="landing-button landing-button-primary">Open Dashboard</Link>
                <Link to="/roadmap" className="landing-button landing-button-secondary">View Roadmap</Link>
              </>
            ) : (
              <>
                <Link to="/register" className="landing-button landing-button-primary">Create Account</Link>
                <Link to="/roadmap" className="landing-button landing-button-secondary">Explore Topics</Link>
              </>
            )}
          </div>
        </div>

        <div className="landing-hero-panel">
          <div className="landing-panel-card">
            <span className="landing-panel-label">What this project does</span>
            <ul>
              <li>Teaches algorithm patterns with structured content</li>
              <li>Lets users practice coding problems in the browser</li>
              <li>Uses AI to explain mistakes and suggest next steps</li>
            </ul>
          </div>
          <div className="landing-stat-grid">
            <div className="landing-stat-card">
              <strong>89</strong>
              <span>Practice Problems</span>
            </div>
            <div className="landing-stat-card">
              <strong>13</strong>
              <span>Algorithm Topics</span>
            </div>
            <div className="landing-stat-card">
              <strong>4</strong>
              <span>Languages</span>
            </div>
            <div className="landing-stat-card">
              <strong>3</strong>
              <span>Hint Levels</span>
            </div>
          </div>
        </div>
      </section>

      <section className="landing-section">
        <div className="landing-section-heading">
          <p className="landing-section-kicker">Overview</p>
          <h2>Built for focused interview preparation</h2>
          <p>
            The platform is meant to reduce context switching. Instead of reading theory in one place,
            coding in another, and asking AI somewhere else, users can do the full loop here.
          </p>
        </div>
        <div className="landing-highlight-grid">
          {highlights.map((item) => (
            <article key={item.title} className="landing-card">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-section landing-section-alt">
        <div className="landing-section-heading">
          <p className="landing-section-kicker">Core Features</p>
          <h2>What users can do inside the product</h2>
        </div>
        <div className="landing-capability-list">
          {capabilities.map((item) => (
            <div key={item} className="landing-capability-item">
              <span className="landing-capability-mark" aria-hidden="true" />
              <p>{item}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="landing-section">
        <div className="landing-section-heading">
          <p className="landing-section-kicker">How It Works</p>
          <h2>A simple learning loop</h2>
        </div>
        <div className="landing-step-grid">
          {steps.map((step) => (
            <article key={step.number} className="landing-step-card">
              <span>{step.number}</span>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-cta">
        <div>
          <p className="landing-section-kicker">Start Here</p>
          <h2>Use the roadmap to learn, then move into problem solving.</h2>
        </div>
        <div className="landing-actions landing-actions-compact">
          <Link to="/roadmap" className="landing-button landing-button-primary">Browse Roadmap</Link>
          <Link to="/code-check" className="landing-button landing-button-secondary">Open Practice Area</Link>
        </div>
      </section>
    </div>
  )
}

export default LandingPage
