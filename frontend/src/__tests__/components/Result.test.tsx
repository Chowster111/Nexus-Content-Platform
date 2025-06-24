import { render, screen } from '@testing-library/react'
import Results from '../../components/Results'
import { ResultItem } from '../../App'

const mockResults: ResultItem[] = [
  {
    title: 'Test Article',
    url: 'https://example.com/article',
    source: 'Example Blog',
    summary: 'A test article about engineering.',
    published_date: new Date().toISOString(),
    category: 'AI',
    tags: ['ml', 'testing'],
  },
]

describe('Results component', () => {
  it('shows loading spinner when loading is true', () => {
    render(<Results results={[]} loading={true} error={null} />)
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('shows error message when error is passed', () => {
    render(<Results results={[]} loading={false} error="Something went wrong" />)
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
  })

  it('renders no results when empty array is passed', () => {
    const { container } = render(<Results results={[]} loading={false} error={null} />)
    expect(container.firstChild).toBeNull()
  })

  it('renders a result card with title, source, and summary', () => {
    render(<Results results={mockResults} loading={false} error={null} />)

    expect(screen.getByText('Test Article')).toBeInTheDocument()
    expect(screen.getByText('Example Blog')).toBeInTheDocument()
    expect(screen.getByText('A test article about engineering.')).toBeInTheDocument()
  })

  it('renders all tags properly', () => {
    render(<Results results={mockResults} loading={false} error={null} />)

    expect(screen.getByText('ml')).toBeInTheDocument()
    expect(screen.getByText('testing')).toBeInTheDocument()
  })
})
