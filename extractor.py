import os
import docx


class Extractor(object):
    def __init__(self, file, doc_extractor=''):
        self.file = file
        self.doc_extractor = os.path.join(doc_extractor, 'antiword') if doc_extractor else self.get_doc_extractor()

    @staticmethod
    def get_doc_extractor():
        """
        获取doc文件提取器的路径
        :return:
        """
        with open('~/antiword-path.txt', 'r') as f:
            return os.path.join(f.readline(), 'antiword')

    @property
    def filename(self):
        """
        get filename
        :return: filename
        """
        return os.path.basename(self.file)

    @property
    def suffix(self):
        """
        后缀
        :return: 后缀
        """
        return os.path.splitext(self.file)[1].lstrip('.')

    def read_txt(self, file=''):
        file = file if file else self.file
        with open(file, 'r') as f:
            content = f.read()
            result = map(lambda x: x.replace(' ', ''), map(lambda x: x.replace('\n', ''), content.split('\n    ')))
            return list(filter(lambda x: x, result))

    def read_doc(self):
        target_file = self.file.replace('doc', 'txt')
        command = '{} {} > {}'.format(self.doc_extractor, self.file, target_file)
        result = os.system(command)
        assert result == 0, '缺少doc提取器antiword, 请检查安装路径%s' % self.doc_extractor
        result = self.read_txt(file=target_file)
        return result

    def read_docx(self):
        content = docx.Document(self.file)
        return list(filter(lambda x: x, map(lambda x: x.text, content.paragraphs)))

    @property
    def content(self):
        """
        获取文本内容
        :return: list of paragraphs
        """
        file_suffix = self.suffix
        try:
            func = self.__getattribute__('read_{}'.format(file_suffix))
        except AttributeError:
            raise AttributeError('{} is Unsupported format'.format(file_suffix))
        return func()


if __name__ == '__main__':
    re = Extractor('离职证明.doc', doc_extractor='/home/zlp/Downloads/antiword-0.37').content
    print(re)
