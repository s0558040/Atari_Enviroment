from gym.envs.registration import register

register(
    id='htw_pong-v0',
    entry_point='atari_games.envs:PongEnv'
)