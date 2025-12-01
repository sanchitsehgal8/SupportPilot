import React, { useState } from 'react'
import api from '../api/client'

export default function SignupPage(){
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSignup(e){
    e.preventDefault()
    setLoading(true)
    setError(null)
    try{
      const res = await api.post('/auth/register', { email, password, name })
      const data = res.data.data
      localStorage.setItem('sp_token', data.token)
      window.location.href = '/customer'
    }catch(err){
      setError(err.response?.data?.error || 'Signup failed')
    }finally{setLoading(false)}
  }

  return (
    <div className="auth-page">
      <form className="auth-form" onSubmit={handleSignup}>
        <h2>Create an account</h2>
        {error && <div className="error">{error}</div>}
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
        <div className="muted">Already have an account? <a href="/login">Login</a></div>
      </form>
    </div>
  )
}
