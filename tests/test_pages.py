from flask_testing import TestCase
from app import create_app


class Test_RenderTemplate(TestCase):
    def create_app(self):
        app = create_app({
                        'TESTING': True,
                        # 'DATABASE': db_path,
                        })
        return app

    render_templates = False

    def test_assert_index_used(self):
        self.client.get("/")
        self.assert_template_used('index.html')

    def test_assert_result_used(self):
        self.client.get("/result/test.jpg")
        self.assert_template_used('result.html')

    def test_assert_thanks_used(self):
        self.client.get("/thanks/test10.jpg&&10")
        self.assert_template_used('thanks.html')

    def test_assert_training_used(self):
        self.client.get("/training/test.jpg")
        self.assert_template_used('training.html')
