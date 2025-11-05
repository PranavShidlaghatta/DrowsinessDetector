import './globals.css'

export const metadata = {
  title: 'Drowsiness Detection',
  description: 'Driver drowsiness monitoring system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}