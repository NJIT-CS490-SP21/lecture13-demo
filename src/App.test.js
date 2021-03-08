import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('Join button disappears', () => {
  const result = render(<App />);

  const joinButtonElement = screen.getByText('Join');
  expect(joinButtonElement).toBeInTheDocument();

  fireEvent.click(joinButtonElement);
  expect(joinButtonElement).not.toBeInTheDocument();
});
