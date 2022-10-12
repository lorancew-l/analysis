import matplotlib.pyplot as plt
from matplotlib import patches

import seaborn as sns
import numpy as np
import pathlib

import argparse

from process import get_salary_by_area, get_specialization_proportions
from common import split_by_thousands, ROLES

sns.set_theme()

AREAS = ['Москва', 'Санкт-Петербург', 'Екатеринбург',
         'Воронеж', 'Новосибирск', 'Самара', 'Омск', 'Челябинск', 'Казань', 'Уфа', 'Новосибирск']

COLORS = ['#94daa5', '#8190c5', '#ec9fc5', '#74baec', '#f4c295', '#f495aa']

ROLE_TRANSLATION = {
    'dev': 'разработчиков',
    'qa': 'тестировщиков',
    'manager': 'менеджеров',
    'analytics': 'аналитиков',
    'sys_admin': 'системных администраторов',
    'design': 'дизайнеров'
}

SPECIALIZATION_TRANSLATION = {
    'frontend': 'Фронтенд разработчик',
    'backend': 'Бэкенд разработчик',
    'mobile': 'Разработчик мобильных приложений',
    'analytics': 'Аналитик',
    'qa': 'Тестировщик',
    'sys_admin': 'Системный администратор'
}


def plot_pie_chart(data, title, output, label_translation_map):
    other = data.pop('other')
    other_color = '#d2d1d2'

    data = dict(
        reversed(sorted(data.items(), key=lambda x: x[1])))

    value_labels = [r'$\bf{' + f'{value}\%' +
                    r'}$' for value in data.values()]
    key_labels = [SPECIALIZATION_TRANSLATION[key]
                  for key in label_translation_map.keys()]
    labels = [*value_labels, *key_labels]

    sizes = data.values()

    colors = [*[COLORS[i] for i in range(len(sizes))], other_color]

    label_markers = [plt.Line2D([0], [0], marker='o', color='w',
                                markerfacecolor=COLORS[i], markersize=15) for i in range(len(sizes))]

    empty_markers = [plt.Line2D([0], [0], marker='o', color='w', alpha=0,
                                markerfacecolor='w', markersize=0) for _ in range(len(sizes))]

    handles = [*label_markers, *empty_markers]

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    ax.pie([*sizes, other], colors=colors, counterclock=False,
           startangle=-270, wedgeprops={'linewidth': 0})
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(centre_circle)

    ax.axis('equal')

    for _ in range(len(sizes)):
        patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor='none',
                          visible=False)

    ax.legend(
        labels=labels,
        loc="center left",
        bbox_to_anchor=(0.85, 0, 0.5, 1),
        frameon=False,
        fontsize=12,
        handles=handles,
        labelspacing=1,
        columnspacing=-1.2,
        handletextpad=0,
        ncols=2
    )

    plt.title(title, loc='left', fontweight='bold', fontsize=18, pad=15)

    if (output):
        fig.savefig(pathlib.Path.cwd() / output)

    plt.tight_layout()
    plt.show()


def plot_bar_chart(x, y, title, output):
    fig = plt.figure(figsize=(12, 7), dpi=110)
    ax = fig.add_subplot(1, 1, 1)

    y_index = np.arange(len(y))
    min_x = min(x)

    ax.barh(y_index, x, color='#6474bc')

    ax.set_yticks(y_index, labels=y)
    ax.invert_yaxis()

    rects = ax.patches

    for i in range(len(rects)):
        label = f'{split_by_thousands(int(x[i]))} ₽'
        ax.text(min_x / 20,  i, label, ha="left",
                va="center", color='white', fontweight='bold')

    plt.title(title, loc='left', fontweight='bold', fontsize=18, pad=15)

    if (output):
        fig.savefig(pathlib.Path.cwd() / output)

    plt.tight_layout()
    plt.show()


def plot_bar_chart_width_median(data, title, output, label_translation_map):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1)

    bar_width = max(map(lambda x: x['max'], data.values())) * 1.4
    bar_height = 0.4

    data = dict(sorted(data.items(), key=lambda x: x[1]['min']))

    ax.barh([i for i in range(len(data))],
            [bar_width for _ in range(len(data))], color='#efeff0', height=bar_height)

    label_colors = ['#6474bc', '#444a60', '#6474bc']
    label_offset = bar_height / 5

    for index, item in enumerate(data.values()):
        y = index - bar_height / 2
        min_value = item['min']
        median = item['median']
        max_value = item['max']

        ax.add_patch(patches.Rectangle(
            (min_value, y), max_value - min_value, bar_height, color="#6474bc"))

        ax.vlines(median, y, index + bar_height /
                  2, color='#444a60', linewidth=4)

        for index, value in enumerate(item.values()):
            label_y = y - bar_height / 2 - label_offset
            ax.text(value, label_y, f'{value}к', ha="center",
                    va="bottom", color=label_colors[index], fontweight='bold')

    if (output):
        fig.savefig(pathlib.Path.cwd() / output)

    labels = [label_translation_map[key]
              for key in label_translation_map.keys()]
    ax.set_yticklabels(['', *labels])

    ax.grid(False)
    ax.set_xlim(0, bar_width)
    ax.set_facecolor('#ffffff')
    ax.set_xticklabels([])

    plt.title(title, loc='left', fontweight='bold', fontsize=18)
    plt.tight_layout()
    plt.show()


def plot_salary_by_area(settings):
    role = settings.role
    role_translation = ROLE_TRANSLATION.get(role, '')
    title = settings.label if settings.label else f'Зарплаты {role_translation} по городам'
    output = settings.output

    area, salary = get_salary_by_area(AREAS, role)

    plot_bar_chart(salary, area, title, output)


def plot_specializations_proportions(settings):
    proportions = get_specialization_proportions()

    title = settings.label if settings.label else 'Распределение специальностей'
    output = settings.output

    plot_pie_chart(proportions, title, output, SPECIALIZATION_TRANSLATION)


def plot_specializations_salary(settings):
    title = settings.label if settings.label else 'Зарплаты специалистов'
    output = settings.output

    data = {
        'dev': {'min': 90, 'median': 200, 'max': 330, },
        'qa': {'min': 35, 'median': 144, 'max': 250, },
        'dev_ops': {'min': 45, 'median': 95, 'max': 155},
        'sys_admin': {'min': 50, 'median': 118, 'max': 200},
        'manager': {'min': 33, 'median': 75, 'max': 160},
        'design': {'min': 32, 'median': 60, 'max': 120},
    }

    plot_bar_chart_width_median(
        data, title, output, SPECIALIZATION_TRANSLATION)


plot_type_map = {
    'salary_by_area': plot_salary_by_area,
    'specializations_proportions': plot_specializations_proportions,
    'specializations_salary': plot_specializations_salary
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--type', help='Plot type', type=str, required=True, choices=plot_type_map.keys())
    parser.add_argument(
        '-l', '--label', help='Plot label', type=str)
    parser.add_argument(
        '-r', '--role', help='Role', type=str, choices=ROLES.keys())
    parser.add_argument(
        '-o', '--output', help='Output file name', type=str)

    args = parser.parse_args()

    plot_func = plot_type_map[args.type]
    plot_func(args)
