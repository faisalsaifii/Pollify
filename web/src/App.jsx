const App = () => {
	return (
		<div>
			<img
				src='https://i.ibb.co/RNGK4qq/Logo.png'
				height={80}
			/>
			<div className='slack-btn-container'>
				<a href='https://slack.com/oauth/v2/authorize?client_id=5846374025732.5969976109991&scope=commands,chat:write&user_scope='>
					<img
						alt='Add to Slack'
						width={80}
						src='https://platform.slack-edge.com/img/add_to_slack.png'
						srcSet='https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x'
					/>
				</a>
			</div>
		</div>
	)
}

export default App
