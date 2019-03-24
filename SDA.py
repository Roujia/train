#coding:UTF-8
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

#创建降噪自编码器类
class Denosing_AutoEncoder():
    def __init__(self,n_hidden,input_data,corruption_level=0.3):
        self.W=None#输入层到隐含层的权重
        self.b=None#输入层到隐含层的偏置
        self.encode_r=None#隐含层的输出5
        self.layer_size=n_hidden#隐含层节点的个数
        self.input_data=input_data#输入样本
        self.keep_prob=1-corruption_level#特征保持不变的比例
        self.W_eval=None#权重W的值
        self.b_eval=None#偏置b的值

    #降噪自编码器的训练
    def fit(self):
        #输入层节点的个数
        n_visible=(self.input_data).shape[1]
        #输入一张图片用28*28=784的向量表示
        X=tf.placeholder("float",[None,n_visible],name='X')
        #用于将部分输入数据置为0
        mask=tf.placeholder("float",[None,n_visible],name='mask')
        #创建权重和偏置
        W_init_max=4*np.sqrt(6./(n_visible+self.layer_size))
        W_init=tf.random_uniform(shape=[n_visible,self.layer_size],minval=-W_init_max,maxval=W_init_max)

        #编码器
        self.W=tf.Variable(W_init,name='W')#784*500
        self.b=tf.Variable(tf.zeros([self.layer_size]),name='b')#隐含层的偏置
        #解码器
        W_prime=tf.transpose(self.W)
        b_prime=tf.Variable(tf.zeros([n_visible]),name='b_prime')
        tilde_X=mask*X#对输入样本加入噪声
        Y=tf.nn.sigmoid(tf.matmul(tilde_X,self.W)+self.b)#隐含层的输出
        Z=tf.nn.sigmoid(tf.matmul(Y,W_prime)+b_prime)#重构输出
        cost=tf.reduce_mean(tf.pow(X-Z,2))#均方误差
        train_op=tf.train.GradientDescentOptimizer(0.01).minimize(cost)#最小化均方误差

        trX=self.input_data
        #开始训练
        with tf.Session() as sess:
            #初始化所有的参数
            tf.initialize_all_variables().run()
            for i in range(30):
                for start,end in zip(range(0,len(trX),128),range(128,len(trX+1),128)):#len(trX)矩阵秩，start=0,128,256...end=128,256,...
                    input_=trX[start:end]#设置输入,每次输入128个，分批操作
                    mask_np=np.random.binomial(1,self.keep_prob,input_.shape)#设置mask,基于二项分布（n,p,size），当n=1时，为伯努利分布（0-1分布）
                    #开始训练
                    sess.run(train_op,feed_dict={X:input_,mask:mask_np})
                if i%5.0==0:#每隔5次输出一次mask=[1,1,...,1]时的loss
                    mask_np=np.random.binomial(1,1,trX.shape)#此时mask尺寸大小与原来输入尺寸大小一致，因此是trX
                    print("loss function at step %s is %s"%(i,sess.run(cost,feed_dict={X:trX,mask:mask_np})))
            #保存好输入层到隐含层的参数
            self.W_eval=(self.W).eval()
            self.b_eval=(self.b).eval()
            mask_np=np.random.binomial(1,1,trX.shape)
            self.encode_r=Y.eval({X:trX,mask:mask_np})

    #取得降噪自编码器的参数
    def get_value(self):
        return self.W_eval,self.b_eval,self.encode_r

#创建堆叠降噪自编码器类
class Stacked_Denosing_AutoEncoder():
    def __init__(self,hidden_list,input_data_trainX,
                 input_data_trainY,input_data_validX,
                 input_data_validY,input_data_testX,
                 input_data_testY,corruption_level=0.3):
        self.ecod_W=[]#保存网络中每一层的权重
        self.ecod_b=[]#保存网络中每一层的偏置
        self.hidden_list=hidden_list#所有隐含层节点个数的集合
        self.input_data_trainX=input_data_trainX#训练样本的特征
        self.input_data_trainY=input_data_trainY#训练样本的标签
        self.input_data_validX=input_data_validX#验证样本的特征
        self.input_data_validY=input_data_validY#验证样本的标签
        self.input_data_testX=input_data_testX#测试样本的特征
        self.input_data_testY=input_data_testY#测试样本的标签

    #堆叠降噪自编码器类的训练
    def fit(self):
        #1、训练每一个降噪自编码器
        next_input_data=self.input_data_trainX
        for i,hidden_size in enumerate(self.hidden_list):#enumerate(x,start=0->开始计数值(i)，默认为0)
            print ("-------- train the %s sda --------"%(i+1))#i默认为0，因此加1
            dae=Denosing_AutoEncoder(hidden_size,next_input_data)
            dae.fit()
            W_eval,b_eval,encode_eval=dae.get_value()
            self.ecod_W.append(W_eval)
            self.ecod_b.append(b_eval)
            next_input_data=encode_eval#上一个编码器的输出作为下一个编码器的输入

        #2、堆叠：将所有的降噪自编码器输入层-隐含层串联起来，并以训练好的值作为初始值
        n_input=(self.input_data_trainX).shape[1]#垂直方向的尺寸
        n_output=(self.input_data_trainY).shape[1]

        X=tf.placeholder("float",[None,n_input],name='X')
        Y=tf.placeholder("float", [None,n_output], name='Y')

        encoding_w_tmp=[]
        encoding_b_tmp=[]

        last_layer=None
        layer_nodes=[]
        encoder=X
        for i,hidden_size in enumerate(self.hidden_list):
            #以每一个自编码器的值作为初始值
            encoding_w_tmp.append(tf.Variable(self.ecod_W[i],name='enc-w-{}'.format(i)))
            encoding_b_tmp.append(tf.Variable(self.ecod_b[i],name='enc-b-{}'.format(i)))
            encoder=tf.nn.sigmoid(tf.matmul(encoder,encoding_w_tmp[i])+encoding_b_tmp[i])
            layer_nodes.append(encoder)#每一层输出的编码器结果
            last_layer=layer_nodes[i]#最后一层

        #加入少量噪声来打破对称性以及避免0梯度
        last_W=tf.Variable(tf.truncated_normal([last_layer.get_shape()[1].value,n_output],stddev=0.1),name='sm-weights')#从截断的正态分布中输出随机值
        last_b=tf.Variable(tf.constant(0.1,shape=[n_output]),name='sm-biases')
        last_out=tf.matmul(last_layer,last_W)+last_b
        layer_nodes.append(last_out)
        cost_sme=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=last_out,labels=Y))
        train_step=tf.train.GradientDescentOptimizer(0.1).minimize(cost_sme)
        model_predictions=tf.argmax(last_out,1)#返回矩阵横列的最大值，因为每一行代表一张图片
        correct_prediction=tf.equal(model_predictions,tf.argmax(Y,1))#判断对应元素是否相等，对应输出True/False
        acurracy=tf.reduce_mean(tf.cast(correct_prediction,"float"))#张量转换成数据类型

        #3、微调
        trX=self.input_data_trainX
        trY=self.input_data_trainY
        vaX=self.input_data_validX
        vaY=self.input_data_validY
        teX=self.input_data_testX
        teY=self.input_data_testY
        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            for i in range(50):
                for start, end in zip(range(0, len(trX), 128), range(128, len(trX + 1), 128)):
                    sess.run(train_step,feed_dict={X:trX[start:end],Y:trY[start:end]})
                if i%5.0==0:
                    print ("Accuracy at step %s on validation set: %s"%(i,sess.run(acurracy,feed_dict={X:vaX,Y:vaY})))
                    print ("Accuracy at step %s on test set: %s"%(i,sess.run(acurracy,feed_dict={X:teX,Y:teY})))

if __name__ =="__main__":
    #1、导入数据集
    mnist=input_data.read_data_sets("MNIST_data/",one_hot=True)#one_hot表示用非零即1的数组保存图片表示的数值.比如一个图片上写的是0,内存中不是直接存一个0,而是存一个数组[1,0,0,0,0,0,0,0,0,0].
    sda=Stacked_Denosing_AutoEncoder([1000,1000,1000],mnist.train.images,mnist.train.labels,
                                     mnist.validation.images,mnist.validation.labels,
                                     mnist.test.images,mnist.test.labels)
    sda.fit()
