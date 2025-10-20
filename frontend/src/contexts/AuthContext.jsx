import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [subscription, setSubscription] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for stored auth data on app load
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    const storedSubscription = localStorage.getItem('subscription')

    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
      setSubscription(JSON.parse(storedSubscription))
    }
    
    setLoading(false)
  }, [])

  const login = (userData, tokenData, subscriptionData) => {
    setUser(userData)
    setToken(tokenData)
    setSubscription(subscriptionData)
    
    localStorage.setItem('token', tokenData)
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('subscription', JSON.stringify(subscriptionData))
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    setSubscription(null)
    
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('subscription')
  }

  const updateUser = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const updateSubscription = (subscriptionData) => {
    setSubscription(subscriptionData)
    localStorage.setItem('subscription', JSON.stringify(subscriptionData))
  }

  const isAuthenticated = () => {
    return !!token && !!user
  }

  const isSubscriptionActive = () => {
    return subscription?.is_active || false
  }

  const getDaysRemaining = () => {
    return subscription?.days_remaining || 0
  }

  const getPatientLimit = () => {
    return subscription?.patient_limit || 50
  }

  const value = {
    user,
    token,
    subscription,
    loading,
    login,
    logout,
    updateUser,
    updateSubscription,
    isAuthenticated,
    isSubscriptionActive,
    getDaysRemaining,
    getPatientLimit
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
