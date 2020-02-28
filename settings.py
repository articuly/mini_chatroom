# 基本设定
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///chatroom.db"  ## ///为相对路经，////为绝对路经
    SECRET_KEY = "123654"

# 开发环境增加的配置
class DevelopmentConfig(BaseConfig):
    pass

# 生产环境增加的配置
class ProductionConfig(BaseConfig):
    pass

# 配置字典，被app.py导入
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}