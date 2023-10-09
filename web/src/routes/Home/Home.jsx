import { Link } from 'react-router-dom'
import './Home.css'

const Home = () => {
	return (
		<div className='main'>
			<h1>Pollify</h1>
			<p>Amplify the process of decision-making</p>
			<img
				src='https://i.ibb.co/fdHPyf8/Logo-3.png'
				width={200}
			/>
			<div className='slack-btn-container'>
				<a href='https://slack.com/oauth/v2/authorize?client_id=5846374025732.5969976109991&scope=commands,chat:write&user_scope='>
					<img
						alt='Add to Slack'
						width={200}
						src='https://platform.slack-edge.com/img/add_to_slack.png'
						srcSet='https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x'
					/>
				</a>
			</div>
			<div className='links'>
				<Link
					to={'/privacy'}
					className='privacy-link'
				>
					Privacy Policy
				</Link>
				<Link
					to={'/support'}
					className='privacy-link'
				>
					Support
				</Link>
				<Link
					to={'/terms-of-service'}
					className='privacy-link'
				>
					Terms of Service
				</Link>
			</div>
		</div>
	)
}

export default Home
