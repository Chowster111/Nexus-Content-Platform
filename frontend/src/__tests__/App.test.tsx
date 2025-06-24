// __tests__/App.test.tsx
import { render, screen } from '@testing-library/react'
import App from '../App'

// Optionally mock child components if needed (e.g., SearchSection, Results, etc.)

describe('App', () => {
  it('renders the search input label', () => {
    render(<App />)
    expect(screen.getByLabelText(/search any mind, any blog/i)).toBeInTheDocument()
  })

  it('renders the Search button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument()
  })

  it('renders the Swipe Mode toggle', () => {
    render(<App />)
    expect(screen.getByText(/swipe mode/i)).toBeInTheDocument()
  })
})
