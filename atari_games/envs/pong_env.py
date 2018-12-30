import gym
import numpy as np
import os
from gym import error, spaces, utils
from gym.utils import seeding

try:
    import atari_py
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install Atari dependencies by running 'pip install gym[atari]'.)".format(e))

def to_ram(ale):
    ram_size = ale.getRAMSize()
    ram = np.zeros((ram_size),dtype=np.uint8)
    ale.getRAM(ram)
    return ram

class PongEnv(gym.Env, utils.EzPickle):
    metadata = {'render.modes': ['human']}

    def __init__(self, game='pong', obs_type='image', frameskip=(2, 5),
                 repeat_action_probability=0., full_action_space=False):
        """Frameskip should be either a tuple (indicating a random range to
        choose from, with the top value exclude), or an int."""

        utils.EzPickle.__init__(self, game, obs_type, frameskip, repeat_action_probability)
        assert obs_type in ('ram', 'image')

        self.game_path = atari_py.get_game_path(game)
        if not os.path.exists(self.game_path):
            raise IOError('You asked for game %s but path %s does not exist' % (game, self.game_path))
        self._obs_type = obs_type
        self.frameskip = frameskip
        self.ale = atari_py.ALEInterface()
        self.viewer = None

        assert isinstance(repeat_action_probability, (float, int)), "Invalid repeat_action_probability: {!r}".format(
            repeat_action_probability)
        self.ale.setFloat('repeat_action_probability'.encode('utf-8'), repeat_action_probability)

        self.seed()

        self._action_set = (self.ale.getLegalActionSet() if full_action_space
                            else self.ale.getMinimalActionSet())
        self.action_space = spaces.Discrete(len(self._action_set))

        (screen_width, screen_height) = self.ale.getScreenDims()
        if self._obs_type == 'ram':
            self.observation_space = spaces.Box(low=0, high=255, dtype=np.uint8, shape=(128,))
        elif self._obs_type == 'image':
            self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)
        else:
            raise error.Error('Unrecognized observation type: {}'.format(self._obs_type))

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        # Derive a random seed. This gets passed as a uint, but gets
        # checked as an int elsewhere, so we need to keep it below
        # 2**31.
        seed2 = seeding.hash_seed(seed1 + 1) % 2 ** 31
        # Empirically, we need to seed before loading the ROM.
        self.ale.setInt(b'random_seed', seed2)
        self.ale.loadROM(self.game_path)

        return [seed1, seed2]

    def _get_image(self):
        return self.ale.getScreenRGB2()

    def _get_ram(self):
        return to_ram(self.ale)

    def step(self, a):
        reward = 0.0
        action = self._action_set[a]

        if isinstance(self.frameskip, int):
            num_steps = self.frameskip
        else:
            num_steps = self.np_random.randint(self.frameskip[0], self.frameskip[1])
        for _ in range(num_steps):
            #reward += self.ale.act(action)
            reward += self.manipulation_reward(action)
        ob = self._get_obs()

        return ob, reward, self.ale.game_over(), {"ale.lives": self.ale.lives()}

    @property
    def _n_actions(self):
        return len(self._action_set)

    def _get_obs(self):
        if self._obs_type == 'ram':
            return self._get_ram()
        elif self._obs_type == 'image':
            img = self._get_image()
        return img

    def reset(self):
        self.ale.reset_game()
        return self._get_obs()

    def render(self, mode='human'):
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        return self.viewer.isopen

    def manipulation_reward(self, action):
        reward = self.ale.act(action)
        if reward == 1:
            reward *= 10
        elif reward == -1:
            reward *= 5
        else:
            reward *= 0
        return reward