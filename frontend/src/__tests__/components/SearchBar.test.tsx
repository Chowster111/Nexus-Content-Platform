import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import SearchSection from '../../components/SearchSection'

describe('SearchSection', () => {
  it('renders input and button', () => {
    render(<SearchSection onSearch={jest.fn()} />)

    expect(screen.getByLabelText(/search any mind/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument()
  })

  it('calls onSearch and clears input when search button clicked', () => {
    const mockSearch = jest.fn()
    render(<SearchSection onSearch={mockSearch} />)

    const input = screen.getByPlaceholderText(/e\.g\., graphql/i)
    const button = screen.getByRole('button', { name: /search/i })

    fireEvent.change(input, { target: { value: 'AI' } })
    fireEvent.click(button)

    expect(mockSearch).toHaveBeenCalledWith('AI')
    expect((input as HTMLInputElement).value).toBe('')
  })

  it('calls onSearch when Enter key is pressed', () => {
    const mockSearch = jest.fn()
    render(<SearchSection onSearch={mockSearch} />)

    const input = screen.getByPlaceholderText(/e\.g\., graphql/i)
    fireEvent.change(input, { target: { value: 'GraphQL' } })
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter', charCode: 13 })

    expect(mockSearch).toHaveBeenCalledWith('GraphQL')
    expect((input as HTMLInputElement).value).toBe('')
  })
})
