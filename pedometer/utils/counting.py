# -*- coding: utf-8 -*-
import os
import time

import numpy as np
import matplotlib.pyplot as plt


def get_data_three_axis_by_file_path(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines_len = len(lines)
        x = np.zeros(shape=(lines_len, 3))
        y = np.zeros(shape=(lines_len,))

        for i in range(lines_len):
            ns = lines[i][lines[i].find('[')+1: lines[i].find(']')].split(',')
            x[i, 0] = float(ns[0])
            x[i, 1] = float(ns[1])
            x[i, 2] = float(ns[2])
            y[i] = int(ns[3])

    return x, y


def show(x_y_z, labels, file_name, points):

    plt.style.use('seaborn-darkgrid')
    # ggplot

    fig = plt.figure(file_name)
    # ax = fig.add_subplot(1, 1, 1)
    vertical_line = plt.axvline(x=0, color='purple', ls='--')
    horizontal_line = plt.axhline(y=0, color='purple', ls='--')

    def update_labels_line(_labels_line, _labels):
        _new_x = [i for i in range(len(_labels)) if _labels[i] == 1]
        _labels_line.set_xdata(_new_x)
        _labels_line.set_ydata([15 for _ in range(len(_new_x))])
        fig.canvas.draw_idle()

    labels_line = plt.plot([], [], 's', color='blue')[0]
    mark = plt.plot([], [], 's', color='green')[0]

    update_labels_line(labels_line, labels)

    def on_key_press(event):
        if event.key == 'a' or event.key == 'd':
            try:
                change_index = int(vertical_line.get_xdata())
                labels[change_index: change_index+4] = 1 if event.key == 'a' else 0
                # ax.lines.remove(ax.lines[-1])
            except (TypeError, Exception):
                pass
            update_labels_line(labels_line, labels)
        elif event.key == 'q' or event.key == 'e':
            try:
                cur_index = int(vertical_line.get_xdata())
                move_len = -1 if event.key == 'q' else 1
                vertical_line.set_xdata(cur_index + move_len)

                if labels[cur_index] == 1:
                    head_index = cur_index
                    rear_index = cur_index

                    while labels[head_index] == 1:
                        head_index = head_index - 1
                    head_index = head_index + 1

                    while labels[rear_index] == 1:
                        rear_index = rear_index + 1

                    labels[head_index: rear_index] = 0
                    labels[head_index + move_len: rear_index + move_len] = 1

                update_labels_line(labels_line, labels)
            except TypeError:
                pass
        elif event.key == 'left' or event.key == 'right':
            try:
                ax_temp = event.inaxes
                x_min, x_max = ax_temp.get_xlim()
                # delta = int((x_max - x_min) * 0.5) * (-1 if event.key == 'left' else 1)
                delta = 5 * (-1 if event.key == 'left' else 1)
                ax_temp.set(xlim=(x_min + delta, x_max + delta))
                cur_index = int(vertical_line.get_xdata())
                vertical_line.set_xdata(cur_index + delta)
            except (TypeError, Exception):
                pass
            # update_labels_line(labels_line, labels)
        elif event.key == 'z' or event.key == 'x' or event.key == 'c' or event.key == 'v':
            try:
                ax_temp = event.inaxes
                x_min, x_max = ax_temp.get_xlim()
                cur_index = int(vertical_line.get_xdata())
                # delta = int((x_max - x_min) * 0.5) * (-1 if event.key == 'left' else 1)
                if event.key == 'z':
                    points[0] = cur_index
                    # print(points[0])
                elif event.key == 'x':
                    points[1] = cur_index
                    # print(points[1])
                elif event.key == 'c':
                    print(points)
                elif event.key == 'v':
                    save_path = os.path.join(slices_path, str(cur_time) + str(1) + str(points[2]).zfill(2) + '.csv')

                    save_file(test_data_x[points[0]:points[1]], labels[points[0]:points[1]], save_path)
                    points[2] += 1

            except (TypeError, Exception):
                pass
            fig.canvas.draw_idle()

    def on_scroll(event):
        try:
            ax_temp = event.inaxes
            x_min, x_max = ax_temp.get_xlim()
            delta = (x_max - x_min) / 10
            if event.button == 'up':
                ax_temp.set(xlim=(x_min + delta, x_max - delta))
                # print("up", event.inaxes)
            elif event.button == 'down':
                ax_temp.set(xlim=(x_min - delta, x_max + delta))
            fig.canvas.draw_idle()
        except (TypeError, AttributeError):
            pass

    def motion(event):
        try:
            vertical_line.set_xdata(int(event.xdata))
            horizontal_line.set_ydata(event.ydata)
            fig.canvas.draw_idle()
        except TypeError:
            pass

    fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)  # 取消默认快捷键的注册
    fig.canvas.mpl_connect('scroll_event', on_scroll)
    fig.canvas.mpl_connect('motion_notify_event', motion)
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    new_x_y_z = x_y_z.T
    xyz = np.sqrt(new_x_y_z[0] ** 2 + new_x_y_z[1] ** 2 + new_x_y_z[2] ** 2)

    plt.plot(new_x_y_z[0], color='r', label='x')
    plt.plot(new_x_y_z[1], color='y', label='y')
    plt.plot(new_x_y_z[2], color='skyblue', label='z')
    plt.plot(xyz, color='black', label='xyz')

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    figManager.toolbar.pan()
    plt.tight_layout()

    plt.rcParams['figure.dpi'] = 100
    # plt.grid()
    plt.legend(loc='upper left')
    plt.show()


def save_file(data, labels, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        rewrite_lines = []
        for _ in range(len(data)):
            rewrite_lines.append(
                '%f, %f, %f, %d\n' % (data[_][0], data[_][1], data[_][2], labels[_]))
        file.writelines(rewrite_lines)


if __name__ == '__main__':
    '''
    
    '''
    slice_point = [0, 0, 0]
    slices_path = r'_'

    test_root = r'F:\wangpengfei\PycharmProjects\swim_data_gan\data\pedometer'
    files = os.listdir(test_root)

    for i, f in enumerate(files):
        cur_time = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))

        slice_point[2] = 0
        print(f)
        f = os.path.join(test_root, f)

        test_data_x, test_data_y = get_data_three_axis_by_file_path(f)
        show(test_data_x, test_data_y, f, slice_point)
        save_file(test_data_x, test_data_y, f)

