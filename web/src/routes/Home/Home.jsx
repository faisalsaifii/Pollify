import { Link } from 'react-router-dom'
import './Home.css'

const Home = () => {
	return (
		<div className='main'>
			<h1>Poll Star</h1>
			<p>Creates Polls like a Star</p>
			<img
				src='https://i.ibb.co/RNGK4qq/Logo.png'
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
			<Link
				to={'/privacy'}
				className='privacy-link'
			>
				Privacy Policy
			</Link>
		</div>
	)
}

export default Home
