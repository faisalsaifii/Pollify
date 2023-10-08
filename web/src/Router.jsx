import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Home from './routes/Home/Home.jsx'
import Privacy from './routes/Privacy.jsx'

const Router = () => {
	const router = createBrowserRouter([
		{
			path: '/',
			element: <Home />,
		},
		{
			path: `/privacy`,
			element: <Privacy />,
		},
	])
	return <RouterProvider router={router} />
}

export default Router
