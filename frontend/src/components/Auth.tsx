'use client'

import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export default function Auth() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const { user, signIn, signUp, signOut } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (isSignUp) {
        await signUp(email, password)
        alert('Sign up successful! Please check your email for verification.')
      } else {
        await signIn(email, password)
      }
    } catch (error) {
      console.error('Error:', error)
      alert(`Error: ${error.message}`)
    }
  }

  if (user) {
    return (
      <div>
        <p>Signed in as: {user.email}</p>
        <Button onClick={signOut}>Sign Out</Button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <Input
        type="password"
        placeholder="Enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <Button type="submit">{isSignUp ? 'Sign Up' : 'Sign In'}</Button>
      <Button type="button" variant="outline" onClick={() => setIsSignUp(!isSignUp)}>
        {isSignUp ? 'Switch to Sign In' : 'Switch to Sign Up'}
      </Button>
    </form>
  )
}

