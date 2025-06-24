import { render, screen, fireEvent } from '@testing-library/react'
import SwipeToggle from '../../components/SwipeToggle'

describe('SwipeToggle', () => {
  it('displays "Swipe" when enabled', () => {
    render(<SwipeToggle enabled={true} onToggle={jest.fn()} />)
    expect(screen.getByText(/swipe/i)).toBeInTheDocument()
  })

  it('displays "List" when disabled', () => {
    render(<SwipeToggle enabled={false} onToggle={jest.fn()} />)
    expect(screen.getByText(/list/i)).toBeInTheDocument()
  })

  it('calls onToggle with opposite value on click', () => {
    const mockToggle = jest.fn()
    render(<SwipeToggle enabled={false} onToggle={mockToggle} />)

    fireEvent.click(screen.getByText(/list/i)) // or fireEvent.click(screen.getByTestId() if you add one)
    expect(mockToggle).toHaveBeenCalledWith(true)
  })
})
