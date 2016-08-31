#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from datetime import date as date_class
from random import randint
from time import localtime, strftime, time

from networkx import Graph

from compute.classes import User, Product, Review


def select() -> int:
    while True:
        try:
            selection = int(input('<Input> The Number of Data or 0 for All Data\n'))
            if selection >= 0:
                return selection
        except ValueError:
            pass
        print('InputError: Invalid Input\a\n')


def get_data(selection=0, table='dianpingcontent'):
    """
     Usage : Get Data from MySQL
     Input : The Data Number You want to get
     OutPut: A List of each record,you should use like this,
            e.g.

            for i in Data:      # i means each record
            [id,name_id,name,contribution,userinforank,review,time,shop,rst1,rst2,rst3]
                for j in i:     # j means each element,t
            class : <'unicode'> except id is <int>
    """
    print('Collecting Data')
    from pymysql import connect
    database = connect(host='localhost', user='root', passwd='1111', db='dianping', charset='utf8')
    cursor = database.cursor()
    try:
        if selection == 0:
            cursor.execute('SELECT * FROM ' + table)
        else:
            cursor.execute('SELECT * FROM ' + table + ' LIMIT ' + str(selection))
        data = cursor.fetchall()
        print('Data is Ready')
    finally:
        cursor.close()
        database.close()
    return data


def set_data(graph=Graph, number=0):
    from pymysql import connect
    database = connect(host='localhost',
                       user='root',
                       password='1111',
                       db='opinion_spam_detection',
                       charset='utf8')
    cursor = database.cursor()
    name = 'dianping_%d_%s' % (number, strftime('%Y%m%d%H%M%S', localtime(time())))
    try:
        cursor.execute('CREATE TABLE  IF NOT EXISTS `%s` '
                       '(`id` INT NOT NULL,'
                       '`class` VARCHAR(1) NOT NULL,'  # U/R/P
                       '`neighbor` TEXT,'  # str(list())
                       '`txt` TEXT NOT NULL,'  # {U:'[name,nameid]',P:'name',R:'[date,star,text]'}
                       '`feature` TEXT,'
                       '`prior` FLOAT NOT NULL,'  # prior[0]
                       '`belief` FLOAT NOT NULL,'  # belief[0]
                       'PRIMARY KEY (`id`))'
                       'ENGINE=InnoDB '
                       'DEFAULT CHARSET=utf8 '
                       'COLLATE utf8_general_ci;'
                       % name)
        for node in graph.nodes():
            neighbor_list = [neighbor.id_number for neighbor in graph.neighbors_iter(node)]

            if isinstance(node, User):
                cursor.execute('INSERT INTO `%s` '
                               '(`id`, `class`, `neighbor`, `txt`, `feature`, `prior`, `belief`) '
                               'VALUES '
                               '(%d, "%s", "%s", "%s", "%s", %f, %f);' %
                               (name,
                                node.id_number,
                                "U",
                                str(neighbor_list),
                                str([node.name, node.name_id]),
                                str(node.feature_value),
                                node.prior[0],
                                node.belief[0]))

            elif isinstance(node, Review):
                # "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute('INSERT INTO `%s` '
                               '(`id`, `class`, `neighbor`, `txt`, `feature`, `prior`, `belief`) '
                               'VALUES '
                               '(%d, "%s", "%s", "%s", "%s", %f, %f);' %
                               (name,
                                node.id_number,
                                "R",
                                str(neighbor_list),
                                str([str(node.date), node.star, node.text]),
                                str(node.feature_value),
                                node.prior[0],
                                node.belief[0]))

            elif isinstance(node, Product):
                cursor.execute('INSERT INTO `%s` '
                               '(`id`, `class`, `neighbor`, `txt`, `feature`, `prior`, `belief`) '
                               'VALUES '
                               '(%d, "%s", "%s", "%s", "%s", %f, %f);' %
                               (name,
                                node.id_number,
                                "P",
                                str(neighbor_list),
                                str([node.name]),
                                str(node.feature_value),
                                node.prior[0],
                                node.belief[0]))
        database.commit()
    finally:
        cursor.close()
        database.close()


def data_to_graph(table=""):
    from pymysql import connect
    database = connect(host='localhost',
                       user='root',
                       password='1111',
                       db='opinion_spam_detection',
                       charset='utf8')
    cursor = database.cursor()
    try:
        cursor.execute('SELECT * FROM ' + table)
        data = cursor.fetchall()
    except:
        data = None
        print('No data\a')
    finally:
        cursor.close()
        database.close()
    graph = Graph()
    graph_dict = dict()
    if data is not None:
        for line in data:
            # `id`, `class`, `neighbor`, `txt`, `feature`, `prior`, `belief`
            id_number = line[0]
            class_name = line[1]
            neighbor = eval(line[2])
            txt = eval(line[3])  # {U:'[name,nameid]',P:'name',R:'[date,star,text]'}
            feature = eval(line[4])
            prior = line[5]
            belief = line[6]
            if class_name == "U":
                new_node = User(id_number=id_number, name=txt[0], name_id=txt[1])
            elif class_name == "R":
                date = txt[0]
                date = date_class(year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:]))  # 2012-02-02
                new_node = Review(id_number=id_number, text=txt[2], date=date, rst1=txt[1][0], rst2=txt[1][1],
                                  rst3=txt[1][2])
            elif class_name == "P":
                new_node = Product(id_number=id_number, name=txt[0])
            else:
                raise NameError
            new_node.neighbor = neighbor
            new_node.feature_value = feature
            new_node.prior = [prior, 1 - prior]
            new_node.belief = [belief, 1 - belief]
            graph_dict[id_number] = new_node
            graph.add_node(new_node)
    for node in graph.nodes():
        for neighbor in node.neighbor:
            graph.add_edge(node, graph_dict[neighbor])
        del node.neighbor
    return graph


def unicode_to_datetime(uni_str='') -> date_class:
    length = len(uni_str)
    if length == 5:
        year = 2016
        month = int(uni_str[0]) * 10 + int(uni_str[1])
        day = int(uni_str[3]) * 10 + int(uni_str[4])
    elif length == 8:  # 15-08-16
        year = 2000 + int(uni_str[0]) * 10 + int(uni_str[1])
        month = int(uni_str[3]) * 10 + int(uni_str[4])
        day = int(uni_str[6]) * 10 + int(uni_str[7])
    else:
        year = randint(2005, 2012)
        month = randint(1, 12)
        day = randint(1, 28)
        print('no date, may use some random number\a')
    return date_class(year, month, day)


def clear_text(text='') -> str:
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '\"')
    text = text.replace('<br/>', ' ')
    return text


# def clear_name(text=''):
#     text = text.replace(' ', '')
#     text = text.replace('\n', '')
#     text = text.replace('...', '')
#     return text


def rst_to_int(uni_str='') -> int:
    try:
        return int(uni_str[2])
    except ValueError:
        return 2


class DataManager(object):
    def __init__(self, number=0):
        self.data = get_data(number)
        self.count = 0
        self.max_num = len(self.data)
        self.line = self.data[self.count]
        self.id_assign = 0

    def get_next_user(self) -> User:
        self.id_assign += 1
        return User(id_number=self.id_assign, name_id=int(self.line[1]), name=self.line[2])

    def get_next_review(self) -> Review:
        self.id_assign += 1
        return Review(id_number=self.id_assign, text=clear_text(self.line[5]),
                      date=unicode_to_datetime(self.line[6]),
                      rst1=rst_to_int(self.line[9]),
                      rst2=rst_to_int(self.line[10]), rst3=rst_to_int(self.line[11]))

    def get_next_product(self) -> Product:
        self.id_assign += 1
        return Product(id_number=self.id_assign, name=self.line[7])

    def next_line(self):
        try:
            self.count += 1
            if self.count < self.max_num:
                self.line = self.data[self.count]
        except IndexError:
            print('No More Data')


def build_graph(graph=Graph(), number=0):
    data_manager = DataManager(number)
    max_data = len(data_manager.data)
    start_time = time()
    print('Get ' + str(max_data) + ' Data')
    print('Building Graph')
    node_dict = dict()
    for i in range(max_data):
        user = data_manager.get_next_user()
        review = data_manager.get_next_review()
        product = data_manager.get_next_product()
        if (user.__class__, user.name, user.name_id) in node_dict:
            user = node_dict[(user.__class__, user.name, user.name_id)]
        else:
            node_dict[(user.__class__, user.name, user.name_id)] = user
        if (product.__class__, product.name) in node_dict:
            product = node_dict[(product.__class__, product.name)]
        else:
            node_dict[(product.__class__, product.name)] = product
        data_manager.next_line()
        # In NetworkX, the implement of node is dict.
        # The implement of dict is hash.
        # In list, two same-data but diff-address objects are the same.
        # In dict, two same-data but diff-address objects are different unless __hash__() is re-defined
        graph.add_node(review)
        graph.add_node(user)
        graph.add_node(product)
        graph.add_edge(user, review)
        graph.add_edge(review, product)
    print('Graph is Ready')
    print('Time Spent on Building Graph : %f' % (time() - start_time))


def show_result(graph=Graph(), mode='cmd'):
    node_count = node_statistic(graph)
    node_count_text = 'User_number:%d\n' \
                      'Review_number:%d\n' \
                      'Product_number:%d\n' % \
                      (node_count[0],
                       node_count[1],
                       node_count[2])
    if mode == 'cmd':
        from os import system
        usage = '-----------------------------\n' \
                'Opinion Spam Detection System\n' \
                '-----------------------------\n' \
                'Command : \n' \
                '    load : load computed data from database\n' \
                '    save : save info of all nodes in a database/txt\n' \
                '    show : show info of all nodes\n' \
                '    select : input an id and get a result\n' + \
                '    about : show more info about selected node\n' + \
                '    sort : sort all the nodes\n' \
                '    usage : print usage\n' \
                '    clear : clear your terminal\n' \
                '    quit : exit this program'
        print(usage)
        cur_node = None
        graph_list = graph.nodes()
        graph_dict = {node.id_number: node for node in graph.nodes()}
        graph_list.sort(key=lambda node: node.belief[0])

        while True:
            command = str(input('>>> '))

            if command == 'quit':
                print('... Bye')
                break

            elif command == 'save':
                type = str(input("... choose a type : 1->Database 2->Text "))
                if type == "1":
                    set_data(graph=graph, number=node_count[1])
                elif type == "2":
                    try:
                        file = open(
                            'records-' + str(node_count[1]) + strftime('-%Y%m%d%H%M%S', localtime(time())) + '.txt',
                            'w', encoding='utf-8')
                        file.write(node_count_text)
                        for node in graph_list:
                            file.write(node.__str__())
                    except UnicodeEncodeError:
                        print('UnicodeEncodeError')
                    finally:
                        file.close()
                else:
                    print("CommandError\a")
                    
            elif command == "load":
                print("... warning : if you load a table, you will lose your current used table")
                table = str(input("... input the table's name "))
                graph = data_to_graph(table=table)
                graph_list = graph.nodes()
                graph_dict = {node.id_number: node for node in graph.nodes()}
                graph_list.sort(key=lambda node: node.belief[0])

            elif command == 'show':
                print(node_count_text)
                for node in graph_list:
                    print(node)

            elif command == 'select':
                try:
                    id_number = int(input('... input id '))
                    if id_number in graph_dict:
                        cur_node = graph_dict[id_number]
                        print(cur_node)
                    else:
                        print('This id do not exist')
                except ValueError:
                    print('CommandError')

            elif command == 'about':
                if cur_node is None:
                    print('You should search a node and then show its more info')
                else:
                    print('current node:')
                    print(cur_node)
                    print(str(len(graph.neighbors(cur_node))) + ' neighbor(s)')
                    for neighbor in graph.neighbors(cur_node):
                        print(neighbor)

            elif command == 'sort':
                try:
                    selection = int(input('... mode : 0->greater 1->less '))
                    graph_list.sort(key=lambda node: node.belief[selection])
                except:
                    print('InputError\a')

            elif command == 'usage':
                print(usage)

            elif command == 'clear':

                system('reset')
                print(usage)

            else:
                print('CommandError')

    elif mode == 'simple':
        for node in graph.nodes():
            print(node)

    elif mode == 'ui':
        pass
    elif mode == 'net':
        pass
    elif mode == 'no':
        print('Show Nothing')
    else:
        raise ValueError('No such a mode called' + mode)


#
# def plot_graph(graph=Graph()):
#     from matplotlib import pyplot
#     from networkx import draw
#     draw(graph)
#     pyplot.show('graph.png')
#     pyplot.show()


def say_finish(times=1):
    print('This program is finish')
    from sys import platform
    if platform == 'darwin':
        voice_list = ['Allison', 'Daniel', 'Samantha']
        for i in range(times):
            from os import system
            system('say -v %s This program is finish' % voice_list[randint(0, len(voice_list) - 1)])


def node_statistic(graph=Graph()):
    product_number = 0
    review_number = 0
    user_number = 0
    for node in graph.nodes():
        if isinstance(node, Product):
            product_number += 1
        elif isinstance(node, Review):
            review_number += 1
        elif isinstance(node, User):
            user_number += 1
    return [user_number, review_number, product_number]


if __name__ == '__main__':
    say_finish()
