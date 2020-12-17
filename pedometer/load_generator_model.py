import os
import time
import tensorflow as tf
import pedometer.pedometer_generator


def restore_model_ckpt(ckpt_file_path):
    generator_optimizer = tf.keras.optimizers.Adam(1e-4)

    model = pedometer.pedometer_generator.build_generator()
    # print(model.get_weights())
    checkpoint = tf.train.Checkpoint(generator=model,
                                     generator_optimizer=generator_optimizer)
    status = checkpoint.restore(tf.train.latest_checkpoint(ckpt_file_path))
    # print(status)

    noise_dim = 100
    num_examples_to_generate = 20

    seed = tf.random.normal([num_examples_to_generate, noise_dim])

    out_generator = model(seed, training=False)
    print(out_generator.shape)

    cur_time = int(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
    out_path = r'../data/generate_pedometer_result/{}'.format(cur_time)
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    out_path = os.path.join(out_path, 'result_{}.txt')
    for i in range(len(out_generator)):
        write_file(out_generator[i], out_path.format(i))


def write_file(out_data, path):
    with open(path, 'w', encoding='utf-8') as f:
        rewrite_lines = []
        for _ in range(len(out_data)):
            rewrite_lines.append('%f, %f, %f\n' %
                                 (out_data[_][0], out_data[_][1], out_data[_][2]))
        f.writelines(rewrite_lines)


if __name__ == '__main__':
    path = r'ckpt/training_checkpoints_202012141616'
    restore_model_ckpt(path)
