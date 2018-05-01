#!/usr/bin/env python3
import argparse
import sys
from baselines.common.cmd_util import make_mujoco_env
from baselines.common.cmd_util import mujoco_arg_parser, dart_arg_parser
from baselines import bench, logger
from baselines.common import tf_util as U
import multiprocessing
import datetime


def train(env_id, num_timesteps, seed):
    from baselines.ppo1 import mlp_policy, pposgd_simple
    U.make_session(num_cpu=1).__enter__()

    def policy_fn(name, ob_space, ac_space):
        return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space,
                                    hid_size=64, num_hid_layers=2)

    env = make_mujoco_env(env_id, seed)
    pposgd_simple.learn(env, policy_fn,
                        max_timesteps=num_timesteps,
                        timesteps_per_actorbatch=2048,
                        clip_param=0.2, entcoeff=0.0,
                        optim_epochs=10, optim_stepsize=3e-4, optim_batchsize=64,
                        gamma=0.99, lam=0.95, schedule='linear',
                        )
    env.close()


def main():
    args = dart_arg_parser().parse_args()
    time_now = datetime.datetime.now().strftime("%I_%M%p_%B%d%Y")
    logger.configure(dir='./train_log/dart_block_lstm_mlp_ppo_' + time_now)
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)


if __name__ == '__main__':
    main()
