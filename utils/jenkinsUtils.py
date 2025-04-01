'''
pipeline {
    agent any
    parameters {
        // 没有 int、float、dict 类型
        string(name: "Int", defaultValue: "1", description: "Int")
        string(name: "Float", defaultValue: "1.1", description: "Float")
        string(name: "Str", defaultValue: "str", description: "Str")// 短字符串
        text(name: "Text", defaultValue: 'Default text', description: 'Text') // 长字符串
        booleanParam(name: "Bool", defaultValue: false, description: "Bool")
        choice(name: "Choice", choices: ['choice1', 'choice2', 'choice3'], description: 'Choice')
        string(name: "List", defaultValue: "strList_0,strList_1,strList_2", description: "List") // 没有 list 类型
        password(name: 'PassWord', defaultValue: 'Password', description: 'Password')
    }
    stages {
        stage('Parameters') {
            steps {
                script {
                    echo """Parameters:
                            Int: ${params.Int}
                            Float: ${params.Float}
                            Str: ${params.Str}
                            Text: ${params.Text}
                            Bool: ${params.Bool}
                            Choice: ${params.Choice}
                            List: ${params.List}
                            PassWord: ${params.PassWord}
                    """
                }
            }
        }
    }
}
'''

if __name__ == "__main__":
    # 用代码出创建一个jenkins工程是一个伪需求。。。没必要。。。
    print("")
