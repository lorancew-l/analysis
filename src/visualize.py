import matplotlib.pyplot as plt
from matplotlib import patches

import seaborn as sns
import numpy as np
import pathlib

import argparse

from process import get_salary_by_area, get_specialization_proportions, get_specializations_salary, get_specializations_experience
from common import split_by_thousands, ROLES

sns.set_theme()

AREAS = ['Москва', 'Санкт-Петербург', 'Екатеринбург',
         'Воронеж', 'Новосибирск', 'Самара', 'Омск', 'Челябинск', 'Казань', 'Уфа', 'Новосибирск']

COLORS = ['#94daa5', '#8190c5', '#ec9fc5', '#74baec', '#f4c295', '#f495aa', '#d2d1d2']

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
    'sys_admin': 'Системный администратор',
    'other': 'Другие'
}

ROLE_TRANSLATION_NOMINATIVE = {
    'dev': 'Разработчики',
    'qa': 'Тестировщики',
    'manager': 'Менеджеры',
    'analytics': 'Аналитики',
    'sys_admin': 'Системные администраторы',
    'design': 'Дизайнеры',
    'dev_ops': 'DevOps',
    'info_sec': 'Информационная безопасность'
}


def plot_pie_chart(data, title, output, label_translation_map):
    other = data.pop('other')

    data = dict(
        reversed(sorted(data.items(), key=lambda x: x[1])))
    data['other'] = other
    
    labels = [r'$\bf{' + f'{value}\%' + r'}$' + f'   {label_translation_map[key]}' for key, value in data.items()]

    sizes = data.values()

    colors = [COLORS[i] for i in range(len(sizes))]

    label_markers = [plt.Line2D([0], [0], marker='o', color='w',
                                markerfacecolor=COLORS[i], markersize=15) for i in range(len(sizes))]
    handles = label_markers

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    ax.pie(sizes, colors=colors, counterclock=False,
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
        handletextpad=0,
    )

    plt.title(title, loc='left', fontweight='bold', fontsize=18, pad=15)

    if (output):
        fig.savefig(pathlib.Path.cwd() / output)

    plt.tight_layout()
    plt.show()


def plot_bar_chart(x, y, title, output, bar_label=None):
    fig = plt.figure(figsize=(12, 7), dpi=110)
    ax = fig.add_subplot(1, 1, 1)

    y_index = np.arange(len(y))

    ax.barh(y_index, x, color='#6474bc')
    ax.set_yticks(y_index, labels=y)
    ax.invert_yaxis()

    rects = ax.patches

    ticks = ax.get_xticks()
    label_offset = (ticks[1] - ticks[0]) / 25

    for i in range(len(rects)):
        label = bar_label(x[i]) if bar_label else x[i]
        ax.text(label_offset,  i, label, ha="left",
                va="center", color='white', fontweight='bold')

    plt.title(title, loc='left', fontweight='bold', fontsize=18, pad=15)

    if (output):
        fig.savefig(pathlib.Path.cwd() / output)

    plt.tight_layout()
    plt.show()


def plot_bar_chart_width_median(data, title, output, label_translation_map=None):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1)

    bar_width = max(map(lambda x: x['max'], data.values())) * 1.1
    bar_height = 0.4

    data = dict(sorted(data.items(), key=lambda x: x[1]['min']))

    ax.barh([i for i in range(len(data))],
            [bar_width for _ in range(len(data))], color='#efeff0', height=bar_height)

    label_colors = ['#6474bc', '#444a60', '#6474bc']
    label_offset = bar_height / 2

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

    if label_translation_map: labels = [label_translation_map[key] for key in label_translation_map.keys()]
    else:  labels = [str(key) for key in data.keys()]

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

    plot_bar_chart(salary, area, title, output, bar_label=lambda x: f'{split_by_thousands(int(x))} ₽')


def plot_specializations_proportions(settings):
    proportions = get_specialization_proportions()

    title = settings.label if settings.label else 'Распределение специальностей'
    output = settings.output
    plot_pie_chart(proportions, title, output, SPECIALIZATION_TRANSLATION)


def plot_specializations_salary(settings):
    title = settings.label if settings.label else 'Зарплаты специалистов'
    output = settings.output
    data = get_specializations_salary()

    plot_bar_chart_width_median(data, title, output, ROLE_TRANSLATION_NOMINATIVE)

def plot_specializations_experience(settings):
    role = settings.role

    vacancy_count_by_experience =  get_specializations_experience(role)
    experience_list = ['Нет опыта', '1-3 года', '3-6 лет', '6+ лет']

    role_translation = ROLE_TRANSLATION.get(role, '')
    title = settings.label if settings.label else f'Количество вакансий по опыту для {role_translation}'
    output = settings.output

    plot_bar_chart(vacancy_count_by_experience, experience_list, title, output, bar_label=lambda x: f'{int(x * 100 / sum(vacancy_count_by_experience))}%')

plot_type_map = {
    'salary_by_area': plot_salary_by_area,
    'specializations_proportions': plot_specializations_proportions,
    'specializations_salary': plot_specializations_salary,
    'specializations_experience': plot_specializations_experience
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
