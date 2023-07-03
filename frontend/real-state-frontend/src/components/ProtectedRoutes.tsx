import { Navigate, Outlet } from 'react-router-dom';
import { useCookie } from '../hooks/useCookie';


const ProtectedRoutes = () => {
  const [cookieValue, _] = useCookie('credentials');
  if (!cookieValue) return (<Navigate to='/home' />)

  const { token } = cookieValue;
  if (!token) return (<Navigate to='/home' />)
  return (
    <Outlet />
  )
}

export default ProtectedRoutes;