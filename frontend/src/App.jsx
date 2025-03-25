import React from 'react'
import Login from './auth/login/Login'
import { NavLink } from 'react-router'

const App = () => {
  return (
    <div>
      <NavLink to='/login'>
        Login
      </NavLink>
    </div>
  )
}

export default App