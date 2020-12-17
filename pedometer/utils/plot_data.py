# -*- coding: utf-8 -*-
import numpy as np
import os
import csv
import matplotlib.pyplot as plt


def csv_get_data_nine_axis_by_file_path(path):
    with open(path, 'r', encoding='utf-8') as csv_f:
        reader = csv.reader(csv_f)
        result = list(reader)
        x = np.zeros(shape=(len(result), 6))
        y = np.zeros(shape=(len(result),))
        for row_num in range(len(result)):
            for col_num in range(3):
                x[row_num, col_num] = float(result[row_num][col_num])
            y[row_num] = 0

    return x, y


def show(x_y_z, labels, style=0, mark_len=0):
    color_list = ['blue', 'purple', 'orange', 'darkgreen', 'darkgoldenrod', 'darkorange']
    fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    vertical_line = plt.axvline(x=0, color='purple', ls='--')
    horizontal_line = plt.axhline(y=0, color='purple', ls='--')

    def update_labels_line(label_lines):
        for cl in range(1, 7):
            _new_x = [i for i in range(len(labels)) if labels[i] == cl]
            label_lines[cl - 1].set_xdata(_new_x)
            label_lines[cl - 1].set_ydata([15 for _ in range(len(_new_x))])
        fig.canvas.draw_idle()

    label_lines = []
    for cl in range(1, 7):
        label_line = plt.plot([], [], 's', color=color_list[cl - 1])[0]
        label_lines.append(label_line)
    update_labels_line(label_lines)

    def on_key_press(event):
        if event.key == 'a' or event.key == 'd':
            try:
                change_index = int(vertical_line.get_xdata())
                labels[change_index: change_index + mark_len] = style if event.key == 'a' else 0
                # ax.lines.remove(ax.lines[-1])
            except (TypeError, Exception):
                pass
            update_labels_line(label_lines)
        elif event.key == '1' or event.key == '2' or event.key == '3' or event.key == '4':
            try:
                change_index = int(vertical_line.get_xdata())
                labels[change_index: change_index + mark_len] = int(event.key)
                # ax.lines.remove(ax.lines[-1])
            except (TypeError, Exception):
                pass
            update_labels_line(label_lines)
        elif event.key == 'q' or event.key == 'e':
            try:
                cur_index = int(vertical_line.get_xdata())
                move_len = -1 if event.key == 'q' else 1
                vertical_line.set_xdata(cur_index + move_len)

                if labels[cur_index] > 0:
                    head_index = cur_index
                    rear_index = cur_index

                    while labels[head_index] > 0:
                        head_index = head_index - 1
                    head_index = head_index + 1

                    while labels[rear_index] > 0:
                        rear_index = rear_index + 1

                    labels[head_index: rear_index] = 0
                    labels[head_index + move_len: rear_index + move_len] = style

                    vertical_line.set_xdata(head_index + move_len)

                update_labels_line(label_lines)
            except TypeError:
                pass

    def on_scroll(event):
        try:
            ax_temp = event.inaxes
            x_min, x_max = ax_temp.get_xlim()
            delta = (x_max - x_min) / 10
            if event.button == 'up':
                ax_temp.set(xlim=(x_min + delta, x_max - delta))
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

    plt.plot(new_x_y_z[0], color='r', label='ax')
    plt.plot(new_x_y_z[1], color='y', label='ay')
    plt.plot(new_x_y_z[2], color='skyblue', label='az')
    plt.plot(xyz, color='black', label='xyz')

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    figManager.toolbar.pan()
    plt.tight_layout()

    plt.grid()
    plt.rcParams['figure.dpi'] = 100
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    style_to_root_dic = {1: r'pedometer_result', 2: r'generate_pedometer_result'}
    marker_style = 2
    marker_root = style_to_root_dic[marker_style]

    test_data_root = r'..\..\data\{}'.format(marker_root)
    dir_list = os.listdir(test_data_root)
    path = os.path.join(test_data_root, dir_list[-1])
    print(path)
    for cur_file in os.listdir(path)[:]:

        test_data_path = os.path.join(path, cur_file)
        print(test_data_path)
        test_data_x, test_data_y = csv_get_data_nine_axis_by_file_path(test_data_path)

        #   0:unknown 1:breaststroke 2:freestyle 3:butterfly 4:backstroke
        show(test_data_x, test_data_y, style=marker_style, mark_len=4)

