from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ebook.com',
                password='admin123',
                role='admin'
            )
            self.stdout.write('Created admin user (admin / admin123)')

        # Create demo user
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user(
                username='demo',
                email='demo@ebook.com',
                password='demo123',
                role='user'
            )
            self.stdout.write('Created demo user (demo / demo123)')

        # Create categories
        from books.models import Category
        categories = [
            'Computer Science', 'Programming', 'Data Science', 'Artificial Intelligence',
            'Web Development', 'Mobile Development', 'Databases', 'Networking',
            'Cybersecurity', 'Software Engineering', 'Mathematics', 'Science',
            'Business', 'Finance', 'Marketing', 'Design',
            'History', 'Philosophy', 'Psychology', 'Self-Help',
            'Fiction', 'Science Fiction', 'Fantasy', 'Mystery',
            'Romance', 'Thriller', 'Horror', 'Biography',
        ]
        cat_objs = {}
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(name=cat_name)
            cat_objs[cat_name] = cat
            if created:
                self.stdout.write(f'  Created category: {cat_name}')

        # Create sample books
        from books.models import Book, BookStats
        import random

        sample_books = [
            # Computer Science & Programming
            {'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'category': 'Computer Science',
             'description': 'A comprehensive introduction to the modern study of computer algorithms. It presents many algorithms and covers them in considerable depth, yet makes their design and analysis accessible to all levels of readers.',
             'price': '39.99', 'tags': 'algorithms,data structures,computer science'},
            {'title': 'Clean Code: A Handbook of Agile Software Craftsmanship', 'author': 'Robert C. Martin',
             'category': 'Programming',
             'description': 'Even bad code can function. But if code isn\'t clean, it can bring a development organization to its knees. This book shows how to write clean, readable, and maintainable code.',
             'price': '29.99', 'tags': 'clean code,programming,software engineering'},
            {'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
             'author': 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides', 'category': 'Software Engineering',
             'description': 'Capturing a wealth of experience about the design of object-oriented software, four top-notch designers present a catalog of simple and succinct solutions to commonly occurring design problems.',
             'price': '34.99', 'tags': 'design patterns,OOP,software design'},
            {'title': 'The Pragmatic Programmer: Your Journey to Mastery', 'author': 'David Thomas, Andrew Hunt',
             'category': 'Programming',
             'description': 'The Pragmatic Programmer cuts through the increasing specialization and technicalities of modern software development to examine the core process of writing code.',
             'price': '32.99', 'tags': 'programming,pragmatic,software development'},
            {'title': 'Structure and Interpretation of Computer Programs', 'author': 'Harold Abelson',
             'category': 'Computer Science',
             'description': 'A classic computer science textbook that teaches the principles of computer programming, including recursion, abstraction, modularity, and programming language design.',
             'price': '45.00', 'tags': 'SICP,programming,computer science'},

            # Data Science & AI
            {'title': 'Deep Learning', 'author': 'Ian Goodfellow, Yoshua Bengio, Aaron Courville',
             'category': 'Artificial Intelligence',
             'description': 'An introduction to a broad range of topics in deep learning, covering mathematical and conceptual background, deep learning techniques used in industry, and research perspectives.',
             'price': '49.99', 'tags': 'deep learning,AI,neural networks'},
            {'title': 'Python for Data Analysis', 'author': 'Wes McKinney', 'category': 'Data Science',
             'description': 'Get complete instructions for manipulating, processing, cleaning, and crunching datasets in Python. Updated for Python 3.10 and pandas 1.4.',
             'price': '27.99', 'tags': 'python,data analysis,pandas'},
            {'title': 'Pattern Recognition and Machine Learning', 'author': 'Christopher M. Bishop',
             'category': 'Artificial Intelligence',
             'description': 'The first textbook on pattern recognition to present the Bayesian viewpoint. This completely new textbook reflects these recent developments while providing a comprehensive introduction to pattern recognition and machine learning.',
             'price': '54.99', 'tags': 'machine learning,pattern recognition,statistics'},
            {'title': 'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow', 'author': 'Aurélien Géron',
             'category': 'Data Science',
             'description': 'Through a series of recent breakthroughs, deep learning has boosted the entire field of machine learning. This book will help you gain an intuitive understanding of the concepts and tools for building intelligent systems.',
             'price': '42.99', 'tags': 'machine learning,scikit-learn,tensorflow,keras'},

            # Web Development
            {'title': 'JavaScript: The Good Parts', 'author': 'Douglas Crockford', 'category': 'Web Development',
             'description': 'Most programming languages contain good and bad parts, but JavaScript has more than its share of the bad. This authoritative book scrapes away these bad features to reveal a subset of JavaScript that is more reliable, readable, and maintainable.',
             'price': '19.99', 'tags': 'javascript,web development,programming'},
            {'title': 'Eloquent JavaScript', 'author': 'Marijn Haverbeke', 'category': 'Web Development',
             'description': 'This much-anticipated third edition of Eloquent JavaScript dives deep into the JavaScript language to show you how to write beautiful, effective code.',
             'price': '24.99', 'tags': 'javascript,web,programming'},
            {'title': 'React: Up & Running', 'author': 'Stoyan Stefanov', 'category': 'Web Development',
             'description': 'Hit the ground running with React, the open source technology from Facebook for building rich web applications fast. Updated for React 18.',
             'price': '28.99', 'tags': 'react,javascript,frontend,web'},

            # Databases
            {'title': 'Designing Data-Intensive Applications', 'author': 'Martin Kleppmann', 'category': 'Databases',
             'description': 'The big ideas behind reliable, scalable, and maintainable systems. This book examines the key principles, algorithms, and trade-offs of data systems.',
             'price': '37.99',
             'tags': 'databases,distributed systems,data engineering'},
            {'title': 'SQL Antipatterns: Avoiding the Pitfalls of Database Programming', 'author': 'Bill Karwin',
             'category': 'Databases',
             'description': 'Each chapter in this book helps you identify, explain, and correct a unique and dangerous antipattern. The four parts of the book group the antipatterns in terms of logical database design, physical database design, queries, and application development.',
             'price': '22.99', 'tags': 'SQL,database,antipatterns'},

            # Cybersecurity
            {'title': 'The Web Application Hacker\'s Handbook', 'author': 'Dafydd Stuttard, Marcus Pinto',
             'category': 'Cybersecurity',
             'description': 'The highly successful security book returns with a new edition, completely updated. Web applications are the front door to most organizations, exposing them to attacks.',
             'price': '31.99', 'tags': 'security,web,hacking'},

            # Fiction & Literature
            {'title': 'Project Hail Mary', 'author': 'Andy Weir', 'category': 'Science Fiction',
             'description': 'Ryland Grace is the sole survivor on a desperate, last-chance mission—and if he fails, humanity and the earth itself will perish.',
             'price': '14.99', 'tags': 'sci-fi,space,adventure'},
            {'title': 'The Midnight Library', 'author': 'Matt Haig', 'category': 'Fiction',
             'description': 'Between life and death there is a library, and within that library, the shelves go on forever. Every book provides a chance to try another life you could have lived.',
             'price': '12.99', 'tags': 'fiction,philosophy,life'},
            {'title': 'Dune', 'author': 'Frank Herbert', 'category': 'Science Fiction',
             'description': 'Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world.',
             'price': '11.99', 'tags': 'sci-fi,classic,adventure'},
            {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy',
             'description': 'Bilbo Baggins is a hobbit who enjoys a comfortable, unambitious life, rarely traveling any farther than his pantry or cellar.',
             'price': '10.99', 'tags': 'fantasy,adventure,classic'},
            {'title': '1984', 'author': 'George Orwell', 'category': 'Fiction',
             'description': 'Among the seminal texts of the 20th century. A startlingly original and haunting novel that creates an imaginary world that is completely convincing.',
             'price': '9.99', 'tags': 'dystopia,classic,politics'},

            # Business & Self-Help
            {'title': 'Atomic Habits', 'author': 'James Clear', 'category': 'Self-Help',
             'description': 'An easy and proven way to build good habits and break bad ones. No matter your goals, Atomic Habits offers a proven framework for improving every day.',
             'price': '16.99', 'tags': 'habits,productivity,self-improvement'},
            {'title': 'Thinking, Fast and Slow', 'author': 'Daniel Kahneman', 'category': 'Psychology',
             'description': 'In the highly anticipated Thinking, Fast and Slow, Kahneman takes us on a groundbreaking tour of the mind and explains the two systems that drive the way we think.',
             'price': '18.99', 'tags': 'psychology,thinking,decision making'},
            {'title': 'Zero to One: Notes on Startups, or How to Build the Future', 'author': 'Peter Thiel',
             'category': 'Business',
             'description': 'The great secret of our time is that there are still uncharted frontiers to explore and new inventions to create. Zero to One presents an optimistic view of the future of progress.',
             'price': '15.99', 'tags': 'startup,business,innovation'},
            {'title': 'Sapiens: A Brief History of Humankind', 'author': 'Yuval Noah Harari', 'category': 'History',
             'description': 'From a renowned historian comes a groundbreaking narrative of humanity\'s creation and evolution that explores the ways in which biology and history have defined us.',
             'price': '17.99', 'tags': 'history,humanity,society'},
        ]

        for i, book_data in enumerate(sample_books):
            cat = cat_objs.get(book_data.pop('category'))
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    **book_data,
                    'category': cat,
                    'cover_url': f'https://picsum.photos/seed/book{i}/200/300',
                    'download_url': f'https://example.com/downloads/{i + 1}',
                    'publish_date': f'202{random.randint(0, 5)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                }
            )
            if created:
                stats = BookStats.objects.create(book=book)
                stats.view_count = random.randint(50, 5000)
                stats.favorite_count = random.randint(5, 500)
                stats.purchase_count = random.randint(10, 300)
                stats.download_count = random.randint(5, 250)
                stats.calculate_hot_score()
                self.stdout.write(f'  Created book: {book.title}')

        # Create some ratings for demo user
        from books.models import Book
        from ratings.models import Rating
        demo_user = User.objects.get(username='demo')
        books = list(Book.objects.all()[:15])
        for book in books:
            if not Rating.objects.filter(user=demo_user, book=book).exists():
                Rating.objects.create(user=demo_user, book=book, rating=random.randint(3, 5))

        self.stdout.write(self.style.SUCCESS(f'Seed complete! Created {Book.objects.count()} books, {Category.objects.count()} categories'))
        self.stdout.write('Admin login: admin / admin123')
        self.stdout.write('Demo login: demo / demo123')
