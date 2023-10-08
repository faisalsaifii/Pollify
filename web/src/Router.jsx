import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Home from './routes/Home/Home.jsx'
import Privacy from './routes/Privacy.jsx'
import Support from './routes/Support/Support.jsx'

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
		{
			path: `/support`,
			element: <Support />,
		},
	])
	return <RouterProvider router={router} />
}

export default Router
