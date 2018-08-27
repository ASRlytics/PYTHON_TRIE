###
# @usage   字典树
# @author  mw
# @date    2016年08月02日  星期二  08:56:34 
# @param
# @return
#
###
class Trie:
    class TrieNode:
        def __init__(self,item,next = None, follows = None):
            self.item = item
            self.next = next
            self.follows = follows
 
        def __str__(self):
            return str(self.item)
 
        def getnext(self):
            return self.next;
 
        def setnext(self, next):
            self.next = next
 
        def getfollows(self):
            return self.follows
 
        def setfollows(self, follows):
            self.follows = follows;
 
        def getitem(self):
            return self.item;
 
        def setitem(self, item):
            self.item = item;
 
        def __iter__(self):
            yield self;
 
            if (self.follows != None):
                for x in self.follows:
                    yield x;
 
        def iternext(self):
            yield self;
 
            if (self.next != None):
                for x in self.next.iternext():
                    yield x;
 
        #从两个方向观察节点信息，一是从它的后续看，这是看一个单词
        #另一个是从它的兄弟看，这是在这个点的各分支
        def info(self, direction = 0):            
            s = '';
 
            if direction == 0:
                for x in self:
                    s += str(x)+'-->';
            else:
                for x in self.iternext():
                    s += str(x)+'-->';
            
            print(s);
 
    def __init__(self):
        self.start = Trie.TrieNode('^', None, None);
 
    def insert(self,item):
        self.start = Trie.__insert(self.start,item)
 
    def __contains__(self,item):
        return Trie.__contains(self.start,item)
 
    #生成诩根所在的结点
    def __genNode(item):
        if (len(item) == 1):
            return Trie.TrieNode(item[0], None, None);
        elif (len(item) > 1):
            return Trie.TrieNode(item[0], None, Trie.__genNode(item[1:]));
        else:
            return None;        
 
    def __insert(node,item):
        # This is the recursive insert function.
        if (item == None or item == ''):
            return None;
        elif (node == None):
            return Trie.__genNode(str(item));
        elif (node.item == item[0]):
            node.setfollows(Trie.__insert(node.getfollows(), item[1:])); 
        else:                
            node.setnext(Trie.__insert(node.getnext(), item));
 
        return node;
 
    def __contains(node, item):
        # This is the recursive membership test.
        #单词结尾用'$'分隔，当然，如果用其它分隔符，此处必须更改item+'$'
        if Trie.__getNode(node, item) != None:
            return True;
        else:
            return False;
 
    #一般都是从字典的根结点开始遍历才有意义
    def getNode(self, item):                
        return Trie.__getNode(self.start, item);
    
    #找到某一节点
    def __getNode(node, item):
        if item == None or item == '':
            return None;
        elif node == None:
            return None;
        elif node.item != item[0]:
            return Trie.__getNode(node.next, item);
        else:
            if (len(item) > 1):
                return Trie.__getNode(node.follows, item[1:]);
            else:                
                return node;
 
    #取某一结点的所有子结点
    def getChild(self, item):
        node = self.getNode(item);
        
        child = [];
        if (node != None):
            if (node.follows != None):
                child.append(node.follows);
 
                p = node.follows;
 
                while (p.next != None):
                    child.append(p.next);
                    p = p.next;
 
        return child;
 
    #取某一结点的兄弟结点
    def getBrother(self, item):
        if item not in self:
            return [];
        else:
            if (len(item) <= 1):
                root = self.start;
                brothers = [];
 
                for x in root.iternext():
                    brothers.append(x);
                return brothers;
            else:
                return self.getChild(item[:-1]);
        
 
    #取得某一结点的前一结点
    def getPrev(self, item):
        if item not in self:
            return None;
        
        len_ = len(item);
        
        if (len_ <= 0):
            return None;
        elif (len_ == 1):            
            root = self.start;
 
            for x in root.iternext():
                if x.next.item == item:
                    return x;
 
            return None;
        else:
            root = self.getNode(item[:-1]);
            root = root.follows;
            if (root.item == item[-1]):
                return None;
            else:
                for x in root.iternext():
                    if x.next.item == item[-1]:
                        return x;
 
                return None;
 
    #取得父结点
    def getParent(self, item):
        if item not in self:
            return None;
        
        len_ = len(item);
        
        if (len_ <= 1):
            return None;
        else:
            return self.getNode(item[:-1]);       
                
 
    #判断是否第一个孩子
    def isFirstChild(self, item):
        if item not in self:
            return False;
        
        len_ = len(item);
        
        if (len_ <= 1):
            return False;
        else:
            parent = self.getNode(item[:-1]);  
            if parent.follows.item == item[-1]:
                return True;
 
            return False;       
    
 
    #从字典树里删除某一单词
    def delete(self, item):
        node = self.getNode(item);
        
        #词不存在或只是部分，就不操作
        if node == None or node.follows != None:
            return [];
        
        len_ = len(item);
 
        if (len_ < 1): #一般这是不可能的，但有时词典中也有空词的位置
            return [];
        else:
            for i in range(len_, 0, -1):
                s = item[0:i]
                brothers = self.getBrother(s);
                count = len(brothers);
 
                print(s);
                print(count);
 
                if (count > 1):
                    break;
 
            if (len(s) <= 1):
                if count <= 2:
                    #树根要占去一个位置，所以如果根的兄弟不多于两个，这棵树就只有一个词
                    #删掉后就只剩下一个树根了
                    self.start.setnext(None);
                else:
                    prev = self.getPrev(s);
                    prev.setnext(prev.next.next);
            else:
                if (self.isFirstChild(s)):
                    parent = self.getParent(s);
                    parent.setfollows(parent.follows.next);
                else:
                    prev = self.getPrev(s);
                    prev.setnext(prev.next.next);
 
            print('在节点{0}处删除'.format(s));
            return item;
 
    #遍历查看字典
    def dict(self):
        #单词结束的末尾标记
        endChar = '$';
 
        count = 0;
        
        if (self.start != None):            
            cursor = self.start;
 
            #具有后续节点的词段
            dict_1 = [];
            #最终版
            dict_2 = [];
            
            while cursor != None:
                #if (cursor.follows == None):
                if (cursor.follows == None):
                    #过滤掉词尾结束标记
                    dict_2.append(str(cursor.item)[:-1]);
                else:
                    dict_1.append(str(cursor.item));
 
                cursor = cursor.next;
 
            while (len(dict_1) > 0):
                a = dict_1.pop(0);
                
                cursor = Trie.__getNode(self.start, a);
                count+=1;
                if (cursor != None):
                    cursor = cursor.follows;
                    
                    while cursor != None:
                        if (cursor.follows == None):
                            dict_2.append((a+str(cursor.item))[:-1]);
                        else:
                            dict_1.append(a+str(cursor.item));
 
                        cursor = cursor.next;
 
            print('找结点{0}次'.format(count));
            print('字典：', dict_2);
        else:
            print('字典为空');
 
    #从某个结点开始遍历，以这个结点为根的子树所有成员
    def dictFromItem(self, item):
        #单词结束的末尾标记
        endChar = '$';
        count = 0;
 
        if (item == '^'):
            return self.dict();
        
        root = self.getNode(item);
 
        if root == None:
            return [];
        else:     
            #具有后续节点的词段
            dict_1 = [];
            #最终版
            dict_2 = [];
            
            dict_1.append(item);                    
 
            while (len(dict_1) > 0):
                a = dict_1.pop(0);
                
                cursor = Trie.__getNode(self.start, a);
                count+=1;
                if (cursor != None):
                    cursor = cursor.follows;
                    
                    while cursor != None:
                        if (cursor.follows == None):
                            dict_2.append((a+str(cursor.item))[:-1]);
                        else:
                            dict_1.append(a+str(cursor.item));
 
                        cursor = cursor.next;
 
            return dict_2;
 
 
 
