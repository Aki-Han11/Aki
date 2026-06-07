"""
Seed the database with admin/demo users, categories, 1000 books,
50 bot users, and random ratings/reviews.
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

# ── Book title generation data ──
TITLE_POOLS = {
    'Computer Science': [
        ('Algorithms and Data Structures', 'Thomas H. Cormen', 'A comprehensive guide to fundamental algorithms, sorting, searching, graph theory, and computational complexity. Essential reading for every software engineer.'),
        ('Operating System Concepts', 'Abraham Silberschatz', 'Covers process management, memory management, storage, I/O, and security in modern operating systems including Linux and Windows.'),
        ('Computer Networks: A Systems Approach', 'Larry L. Peterson', 'Explores network architecture, protocols, and distributed systems from the ground up with real-world implementation examples.'),
        ('Introduction to the Theory of Computation', 'Michael Sipser', 'Classic text on automata theory, computability, and complexity theory with rigorous proofs and intuitive explanations.'),
        ('Computer Architecture: A Quantitative Approach', 'John L. Hennessy', 'The definitive guide to processor design, memory hierarchy, and parallel computing architectures.'),
        ('Distributed Systems: Principles and Paradigms', 'Andrew S. Tanenbaum', 'Comprehensive coverage of distributed algorithms, consistency models, fault tolerance, and modern cloud infrastructure.'),
        ('Compilers: Principles, Techniques, and Tools', 'Alfred V. Aho', 'The Dragon Book — classic reference on lexical analysis, parsing, semantic analysis, code generation, and optimization.'),
        ('Information Theory and Coding', 'Robert Gallager', 'Fundamental principles of information theory, entropy, channel capacity, and error-correcting codes.'),
        ('Digital Design and Computer Architecture', 'David Harris', 'From logic gates to processor design — a practical approach to building digital systems.'),
        ('Computer Graphics: Principles and Practice', 'James D. Foley', 'Comprehensive coverage of rendering, modeling, animation, and GPU programming techniques.'),
        ('Parallel Computer Architecture', 'David Culler', 'Design principles for scalable multiprocessor systems and parallel programming models.'),
        ('Cryptography and Network Security', 'William Stallings', 'Principles and practices of modern cryptography, authentication, and network security protocols.'),
        ('Artificial Intelligence: A Modern Approach', 'Stuart Russell', 'The leading textbook on AI covering search, logic, planning, machine learning, and robotics.'),
        ('Computer Vision: Algorithms and Applications', 'Richard Szeliski', 'Comprehensive exploration of image processing, feature detection, 3D reconstruction, and deep learning for vision.'),
        ('Introduction to Automata Theory', 'John E. Hopcroft', 'Languages, automata, and computability theory with applications to compiler design and formal verification.'),
        ('Principles of Database Systems', 'Jeffrey D. Ullman', 'Foundational text on relational algebra, normalization, transaction processing, and query optimization.'),
        ('Machine Learning: A Probabilistic Perspective', 'Kevin P. Murphy', 'Rigorous probabilistic approach to machine learning with Bayesian methods, graphical models, and deep learning.'),
        ('Computer Security: Principles and Practice', 'William Stallings', 'Systematic treatment of computer security covering cryptography, software security, and network defense.'),
        ('Data Mining: Concepts and Techniques', 'Jiawei Han', 'Comprehensive guide to data preprocessing, classification, clustering, association analysis, and anomaly detection.'),
        ('Embedded Systems: Real-Time Operating Systems', 'K.V.K.K. Prasad', 'Design and implementation of real-time embedded systems with ARM and RTOS concepts.'),
        ('Software Testing: Principles and Practices', 'Srinivasan Desikan', 'Complete guide to test planning, test case design, automation, and quality assurance methodologies.'),
        ('Cloud Computing: Concepts and Technology', 'Thomas Erl', 'Comprehensive coverage of cloud architecture, virtualization, service models, and deployment strategies.'),
        ('Blockchain Technology: Principles and Applications', 'Arvind Narayanan', 'Technical introduction to blockchain, consensus algorithms, smart contracts, and decentralized applications.'),
        ('Quantum Computing for Computer Scientists', 'Noson S. Yanofsky', 'Accessible introduction to quantum mechanics, qubits, quantum gates, and quantum algorithms.'),
        ('Human-Computer Interaction: Design and Development', 'Alan Dix', 'Principles of user-centered design, usability engineering, and interactive system development.'),
        ('Natural Language Processing with Deep Learning', 'Christopher Manning', 'Modern NLP techniques using neural networks: transformers, BERT, GPT, attention mechanisms.'),
        ('Reinforcement Learning: An Introduction', 'Richard S. Sutton', 'The definitive introduction to reinforcement learning covering bandits, MDPs, TD learning, and deep RL.'),
        ('Ethical Hacking and Penetration Testing', 'Patrick Engebretson', 'Hands-on guide to security assessment, vulnerability analysis, and penetration testing methodologies.'),
        ('Internet of Things: Architecture and Design', 'Arshdeep Bahga', 'End-to-end IoT systems covering sensors, protocols, cloud integration, and data analytics.'),
        ('Software Architecture in Practice', 'Len Bass', 'Proven approaches to designing, documenting, and evaluating software architectures for complex systems.'),
    ],
    'Programming': [
        ('The Pragmatic Programmer', 'David Thomas', 'Timeless advice on software craftsmanship, debugging, refactoring, and professional development.'),
        ('Clean Code', 'Robert C. Martin', 'Principles and practices for writing readable, maintainable, and elegant code in any programming language.'),
        ('Design Patterns: Elements of Reusable Software', 'Erich Gamma', 'The Gang of Four classic — 23 fundamental design patterns for object-oriented software development.'),
        ('Refactoring: Improving the Design of Existing Code', 'Martin Fowler', 'Systematic techniques for restructuring code without changing its external behavior.'),
        ('Code Complete', 'Steve McConnell', 'A practical handbook of software construction covering coding, design, testing, and debugging.'),
        ('Programming Pearls', 'Jon Bentley', 'Insightful essays on elegant algorithms, performance optimization, and pragmatic problem-solving.'),
        ('The Art of Computer Programming', 'Donald E. Knuth', 'The monumental work on algorithmic analysis, combinatorial algorithms, and mathematical foundations.'),
        ('Head First Design Patterns', 'Eric Freeman', 'Visual and engaging introduction to design patterns with Java examples and practical scenarios.'),
        ('Effective Java', 'Joshua Bloch', 'Best practices for the Java platform covering generics, concurrency, serialization, and API design.'),
        ('Python Crash Course', 'Eric Matthes', 'Hands-on project-based introduction to Python programming covering data analysis, web apps, and games.'),
        ('Fluent Python', 'Luciano Ramalho', 'Deep dive into Python data model, functional programming, metaprogramming, and concurrency.'),
        ('JavaScript: The Good Parts', 'Douglas Crockford', 'Unearths the elegant, reliable subset of JavaScript hidden beneath a complex language surface.'),
        ('You Don\'t Know JS', 'Kyle Simpson', 'In-depth exploration of JavaScript mechanics: scope, closures, prototypes, async, and performance.'),
        ('Rust Programming Language', 'Steve Klabnik', 'Official guide to Rust covering ownership, lifetimes, traits, and fearless concurrency.'),
        ('Go Programming Language', 'Alan Donovan', 'The authoritative guide to Go covering idioms, concurrency patterns, and standard library usage.'),
        ('C Programming Language', 'Brian Kernighan', 'The classic K&R book — the definitive reference for C programming fundamentals.'),
        ('Programming in Scala', 'Martin Odersky', 'Comprehensive guide to Scala covering functional programming, OOP, and type system features.'),
        ('Learning TypeScript', 'Josh Goldberg', 'From JavaScript to TypeScript — mastering types, generics, and advanced type system features.'),
        ('Kotlin in Action', 'Dmitry Jemerov', 'Practical guide to Kotlin covering language features, DSLs, coroutines, and Android development.'),
        ('Swift Programming: The Big Nerd Ranch Guide', 'Matthew Mathias', 'Comprehensive Swift programming covering optionals, protocols, generics, and iOS fundamentals.'),
        ('Functional Programming in Scala', 'Paul Chiusano', 'Rigorous introduction to purely functional programming using Scala with real-world applications.'),
        ('Algorithms in C++', 'Robert Sedgewick', 'Practical implementation of fundamental algorithms and data structures in C++.'),
        ('Programming Ruby', 'Dave Thomas', 'The Pickaxe book — comprehensive Ruby language reference and programming guide.'),
        ('Eloquent JavaScript', 'Marijn Haverbeke', 'Beautiful introduction to programming and JavaScript through interactive exercises and projects.'),
        ('Automate the Boring Stuff with Python', 'Al Sweigart', 'Practical Python for everyday automation tasks: files, web scraping, Excel, email, and GUI.'),
        ('Introduction to Programming with Java', 'Y. Daniel Liang', 'Comprehensive Java programming fundamentals with problem-solving and algorithm development.'),
        ('Perl Best Practices', 'Damian Conway', 'Standards and styles for developing maintainable, efficient Perl code in team environments.'),
        ('Haskell Programming from First Principles', 'Christopher Allen', 'Thorough introduction to Haskell and pure functional programming with gradual skill building.'),
        ('PHP and MySQL Web Development', 'Luke Welling', 'Practical guide to building dynamic, database-driven websites with PHP and MySQL.'),
        ('The Linux Programming Interface', 'Michael Kerrisk', 'Comprehensive guide to Linux and UNIX system programming covering all major APIs.'),
    ],
    'Data Science': [
        ('Python for Data Analysis', 'Wes McKinney', 'Complete guide to data manipulation, cleaning, and analysis with pandas, NumPy, and Python.'),
        ('Data Science from Scratch', 'Joel Grus', 'First principles approach to data science building algorithms and tools from the ground up.'),
        ('Storytelling with Data', 'Cole Nussbaumer Knaflic', 'Guide to data visualization and communicating insights effectively through charts and presentations.'),
        ('Practical Statistics for Data Scientists', 'Peter Bruce', 'Essential statistical methods for data science with practical examples in R and Python.'),
        ('Hands-On Machine Learning', 'Aurelien Geron', 'Practical guide to building ML systems with Scikit-Learn, Keras, and TensorFlow.'),
        ('Data Engineering with Python', 'Paul Crickard', 'Building scalable data pipelines, ETL workflows, and data infrastructure with modern Python tools.'),
        ('Introduction to Statistical Learning', 'Gareth James', 'Accessible introduction to statistical learning methods with applications in R.'),
        ('Feature Engineering for Machine Learning', 'Alice Zheng', 'Principles and techniques for creating effective features from raw data.'),
        ('Data Visualization: A Practical Introduction', 'Kieran Healy', 'How to make compelling data visualizations using ggplot2 and the principles of visual perception.'),
        ('Mining of Massive Datasets', 'Jure Leskovec', 'Algorithms and techniques for processing and analyzing web-scale datasets efficiently.'),
    ],
    'Artificial Intelligence': [
        ('Deep Learning', 'Ian Goodfellow', 'Comprehensive mathematical and conceptual foundation of deep learning from the pioneers of the field.'),
        ('Pattern Recognition and Machine Learning', 'Christopher Bishop', 'Rigorous Bayesian treatment of machine learning with probabilistic graphical models.'),
        ('Machine Learning Yearning', 'Andrew Ng', 'Practical strategies for structuring machine learning projects and making technical decisions.'),
        ('Generative Deep Learning', 'David Foster', 'Teaching machines to paint, write, compose music, and create with generative models.'),
        ('Speech and Language Processing', 'Dan Jurafsky', 'Comprehensive NLP textbook covering syntax, semantics, pragmatics, and modern neural approaches.'),
        ('Deep Reinforcement Learning Hands-On', 'Maxim Lapan', 'Practical guide to implementing RL algorithms with PyTorch from DQN to PPO and beyond.'),
        ('Interpretable Machine Learning', 'Christoph Molnar', 'Guide to making black-box models explainable with SHAP, LIME, and partial dependence plots.'),
    ],
    'Web Development': [
        ('Designing Data-Intensive Applications', 'Martin Kleppmann', 'The big ideas behind reliable, scalable, and maintainable data systems for modern web applications.'),
        ('Building Microservices', 'Sam Newman', 'Designing fine-grained systems with evolutionary architecture, deployment, and organizational patterns.'),
        ('High Performance Browser Networking', 'Ilya Grigorik', 'Everything web developers should know about networking, HTTP/2, WebSocket, and WebRTC.'),
        ('Web Scalability for Startup Engineers', 'Artur Ejsmont', 'Practical guide to building scalable web architectures from frontend to backend infrastructure.'),
        ('RESTful Web APIs', 'Leonard Richardson', 'Designing and building hypermedia-driven REST APIs that stand the test of time.'),
        ('OAuth 2.0 Simplified', 'Aaron Parecki', 'Clear and practical guide to OAuth 2.0, OpenID Connect, and secure API authorization flows.'),
    ],
    'Databases': [
        ('Database Internals', 'Alex Petrov', 'Deep dive into how distributed databases work: storage engines, replication, and consensus.'),
        ('SQL Performance Explained', 'Markus Winand', 'Everything developers need to know about SQL performance, indexing, and query optimization.'),
        ('Seven Databases in Seven Weeks', 'Luc Perkins', 'Tour of modern databases: PostgreSQL, MongoDB, Redis, Neo4j, and others with hands-on exercises.'),
        ('High Performance MySQL', 'Baron Schwartz', 'Optimization, backups, replication, and load balancing for MySQL at scale.'),
        ('MongoDB: The Definitive Guide', 'Shannon Bradshaw', 'Comprehensive guide to MongoDB data modeling, aggregation, sharding, and administration.'),
    ],
    'Cybersecurity': [
        ('The Web Application Hacker\'s Handbook', 'Dafydd Stuttard', 'Practical guide to finding and exploiting security flaws in web applications.'),
        ('Metasploit: The Penetration Tester\'s Guide', 'David Kennedy', 'Mastering the Metasploit framework for professional penetration testing engagements.'),
        ('Practical Malware Analysis', 'Michael Sikorski', 'Hands-on guide to dissecting malicious software with debuggers, disassemblers, and sandboxes.'),
        ('Applied Cryptography', 'Bruce Schneier', 'Definitive reference on cryptographic protocols, algorithms, and source code implementations.'),
    ],
    'Mathematics': [
        ('Concrete Mathematics', 'Ronald L. Graham', 'Foundation for computer science covering sums, recurrences, number theory, and generating functions.'),
        ('Linear Algebra Done Right', 'Sheldon Axler', 'Theoretical approach to linear algebra emphasizing vector spaces and linear transformations.'),
        ('Probability Theory: The Logic of Science', 'E.T. Jaynes', 'Bayesian probability as extended logic with applications to statistics, physics, and machine learning.'),
        ('Calculus: Early Transcendentals', 'James Stewart', 'Comprehensive calculus text covering single and multivariable calculus with applications.'),
        ('Discrete Mathematics and Its Applications', 'Kenneth H. Rosen', 'Covering logic, set theory, combinatorics, graph theory, and Boolean algebra for computer science.'),
    ],
    'Physics': [
        ('The Feynman Lectures on Physics', 'Richard P. Feynman', 'Legendary physics lectures covering mechanics, electromagnetism, quantum mechanics, and more.'),
        ('A Brief History of Time', 'Stephen Hawking', 'Accessible exploration of cosmology, black holes, and the search for a unified theory of physics.'),
        ('The Elegant Universe', 'Brian Greene', 'Superstrings, hidden dimensions, and the quest for the ultimate theory of everything.'),
        ('Quantum Mechanics and Path Integrals', 'Richard P. Feynman', 'Feynman\'s revolutionary path integral formulation of quantum mechanics.'),
    ],
    'History': [
        ('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'The sweeping narrative of human history from the Stone Age to the present day.'),
        ('Guns, Germs, and Steel', 'Jared Diamond', 'Why did certain civilizations conquer others? A geographic and environmental history of the world.'),
        ('The Silk Roads', 'Peter Frankopan', 'A new history of the world told through the networks of trade and cultural exchange along the Silk Roads.'),
        ('A People\'s History of the United States', 'Howard Zinn', 'American history from the perspective of ordinary people, dissenters, and marginalized groups.'),
        ('The Rise and Fall of the Third Reich', 'William L. Shirer', 'Comprehensive history of Nazi Germany based on captured documents and personal experience.'),
        ('SPQR: A History of Ancient Rome', 'Mary Beard', 'The story of Rome from its mythical founding to the fall of the Empire.'),
        ('The Crusades: The Authoritative History', 'Thomas Asbridge', 'A gripping account of the Crusades and their lasting impact on Christianity and Islam.'),
        ('1491: New Revelations of the Americas Before Columbus', 'Charles C. Mann', 'The thriving, sophisticated civilizations of the pre-Columbian Americas.'),
    ],
    'Philosophy': [
        ('Meditations', 'Marcus Aurelius', 'The personal philosophical notes of a Roman emperor on Stoic philosophy and the art of living.'),
        ('Beyond Good and Evil', 'Friedrich Nietzsche', 'Nietzsche\'s critique of traditional morality and his vision for a philosophy of the future.'),
        ('The Republic', 'Plato', 'Plato\'s masterpiece on justice, the ideal state, and the nature of reality and knowledge.'),
        ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Nobel laureate\'s exploration of the two systems that drive human thought and decision-making.'),
    ],
    'Psychology': [
        ('Man\'s Search for Meaning', 'Viktor E. Frankl', 'A psychiatrist\'s Holocaust survival story and the foundation of logotherapy.'),
        ('Influence: The Psychology of Persuasion', 'Robert B. Cialdini', 'The six principles of persuasion backed by decades of psychological research.'),
        ('The Power of Habit', 'Charles Duhigg', 'Why habits exist and how they can be transformed to improve lives and organizations.'),
        ('Flow: The Psychology of Optimal Experience', 'Mihaly Csikszentmihalyi', 'The science of happiness and how to achieve it through complete absorption in meaningful activities.'),
    ],
    'Self-Help': [
        ('Atomic Habits', 'James Clear', 'An easy and proven way to build good habits and break bad ones through tiny, incremental changes.'),
        ('The 7 Habits of Highly Effective People', 'Stephen R. Covey', 'Powerful lessons in personal change and leadership based on principles of fairness and integrity.'),
        ('How to Win Friends and Influence People', 'Dale Carnegie', 'Timeless advice on building relationships, winning people over, and becoming a better communicator.'),
        ('Daring Greatly', 'Brene Brown', 'How the courage to be vulnerable transforms the way we live, love, parent, and lead.'),
    ],
    'Business': [
        ('Zero to One', 'Peter Thiel', 'Notes on startups and how to build the future through monopoly and contrarian thinking.'),
        ('The Lean Startup', 'Eric Ries', 'How constant innovation and validated learning create radically successful businesses.'),
        ('Good to Great', 'Jim Collins', 'Why some companies make the leap from good to great and others don\'t.'),
        ('Start with Why', 'Simon Sinek', 'How great leaders inspire everyone to take action by starting with a clear sense of purpose.'),
    ],
    'Finance': [
        ('The Intelligent Investor', 'Benjamin Graham', 'The definitive book on value investing and the philosophy that shaped Warren Buffett.'),
        ('A Random Walk Down Wall Street', 'Burton G. Malkiel', 'The time-tested strategy for successful investing based on efficient market theory.'),
        ('Rich Dad Poor Dad', 'Robert T. Kiyosaki', 'What the rich teach their kids about money that the poor and middle class do not.'),
    ],
    'Economics': [
        ('Freakonomics', 'Steven D. Levitt', 'A rogue economist explores the hidden side of everything using data and incentives.'),
        ('Capital in the Twenty-First Century', 'Thomas Piketty', 'A monumental analysis of wealth and income inequality in Europe and the United States.'),
        ('The Wealth of Nations', 'Adam Smith', 'The foundational text of classical economics and the invisible hand of the market.'),
    ],
    'Political Science': [
        ('The Prince', 'Niccolo Machiavelli', 'The classic treatise on political power, strategy, and statecraft.'),
        ('The Origins of Totalitarianism', 'Hannah Arendt', 'A profound analysis of the nature and origins of totalitarian movements in the 20th century.'),
        ('The Road to Serfdom', 'Friedrich A. Hayek', 'A powerful warning against centralized economic planning and its inevitable slide into tyranny.'),
    ],
    'Science': [
        ('A Short History of Nearly Everything', 'Bill Bryson', 'A fascinating journey through the history of science from the Big Bang to modern discoveries.'),
        ('The Selfish Gene', 'Richard Dawkins', 'The gene-centered view of evolution that revolutionized our understanding of natural selection.'),
        ('Cosmos', 'Carl Sagan', 'A personal voyage through space and time exploring the universe and our place within it.'),
        ('The Double Helix', 'James D. Watson', 'The personal account of the race to discover the structure of DNA.'),
    ],
    'Fiction': [
        ('The Great Gatsby', 'F. Scott Fitzgerald', 'A tale of wealth, love, and the American Dream set in the Jazz Age of the 1920s.'),
        ('To Kill a Mockingbird', 'Harper Lee', 'A profound story of racial injustice and moral growth in the American South.'),
        ('One Hundred Years of Solitude', 'Gabriel Garcia Marquez', 'The multi-generational saga of the Buendia family in the mythical town of Macondo.'),
        ('Crime and Punishment', 'Fyodor Dostoevsky', 'A young intellectual\'s descent into murder and his subsequent psychological and spiritual crisis.'),
        ('Pride and Prejudice', 'Jane Austen', 'A witty social commentary on marriage, class, and morality in Regency-era England.'),
        ('The Catcher in the Rye', 'J.D. Salinger', 'Holden Caulfield\'s unforgettable journey through New York City and adolescent alienation.'),
        ('Don Quixote', 'Miguel de Cervantes', 'The adventures of a delusional knight and his loyal squire in this classic of world literature.'),
        ('War and Peace', 'Leo Tolstoy', 'An epic novel of Russian society during the Napoleonic Wars exploring love, fate, and history.'),
        ('Beloved', 'Toni Morrison', 'A haunting story of a former slave haunted by the ghost of her baby daughter.'),
        ('The Kite Runner', 'Khaled Hosseini', 'A story of friendship, betrayal, and redemption set against the backdrop of Afghanistan\'s turbulent history.'),
    ],
    'Science Fiction': [
        ('Dune', 'Frank Herbert', 'The epic saga of Paul Atreides on the desert planet Arrakis — politics, religion, and ecology.'),
        ('Neuromancer', 'William Gibson', 'The novel that launched cyberpunk — a washed-up hacker hired for one last impossible job.'),
        ('Foundation', 'Isaac Asimov', 'A mathematician predicts the fall of the Galactic Empire and creates a plan to shorten the dark age.'),
        ('Ender\'s Game', 'Orson Scott Card', 'A young genius is trained through war games to become humanity\'s last hope against an alien threat.'),
        ('The Left Hand of Darkness', 'Ursula K. Le Guin', 'A groundbreaking exploration of gender and society on a planet where inhabitants are ambisexual.'),
        ('Snow Crash', 'Neal Stephenson', 'A fast-paced cyberpunk adventure through virtual reality, ancient Sumerian mythology, and corporate dystopia.'),
        ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 'The hilarious intergalactic adventure of Arthur Dent after Earth is destroyed to make way for a hyperspace bypass.'),
        ('Hyperion', 'Dan Simmons', 'Seven pilgrims share their tales on the eve of Armageddon in this Hugo Award-winning space opera.'),
    ],
    'Fantasy': [
        ('The Hobbit', 'J.R.R. Tolkien', 'Bilbo Baggins\' unexpected journey with dwarves and a wizard to reclaim a dragon\'s treasure.'),
        ('A Game of Thrones', 'George R.R. Martin', 'Noble families vie for control of the Iron Throne in a world where summers last decades and winters a lifetime.'),
        ('The Name of the Wind', 'Patrick Rothfuss', 'The tale of Kvothe — magician, musician, and legendary figure — told in his own words.'),
        ('American Gods', 'Neil Gaiman', 'Old gods brought to America by immigrants face a new pantheon of media, technology, and celebrity.'),
        ('The Wizard of Earthsea', 'Ursula K. Le Guin', 'A young wizard\'s coming-of-age story in a world of true names, dragons, and the balance of power.'),
        ('Mistborn: The Final Empire', 'Brandon Sanderson', 'A crew of thieves plans to overthrow a god-emperor in a world where ash falls from the sky.'),
    ],
    'Mystery': [
        ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'A journalist and a brilliant hacker investigate a decades-old disappearance in this gripping thriller.'),
        ('Gone Girl', 'Gillian Flynn', 'A wife disappears on her fifth wedding anniversary — and her husband becomes the prime suspect.'),
        ('The Da Vinci Code', 'Dan Brown', 'A Harvard symbologist uncovers a secret society\'s ancient conspiracy hidden in famous artworks.'),
        ('And Then There Were None', 'Agatha Christie', 'Ten strangers on an island are murdered one by one in the queen of mystery\'s masterpiece.'),
    ],
    'Romance': [
        ('Sense and Sensibility', 'Jane Austen', 'Two sisters navigate love, heartbreak, and societal expectations in this beloved classic of English literature.'),
        ('The Notebook', 'Nicholas Sparks', 'A sweeping love story spanning decades — two people from different worlds whose love endures all.'),
        ('Outlander', 'Diana Gabaldon', 'A World War II nurse mysteriously travels back to 1743 Scotland and finds passion and adventure.'),
        ('Me Before You', 'Jojo Moyes', 'A young woman becomes a caregiver for a paralyzed man and discovers love in unexpected places.'),
    ],
    'Thriller': [
        ('The Silence of the Lambs', 'Thomas Harris', 'FBI trainee Clarice Starling seeks the help of imprisoned cannibal Dr. Lecter to catch a serial killer.'),
        ('The Bourne Identity', 'Robert Ludlum', 'A man with no memory and extraordinary skills must piece together his identity while evading assassins.'),
        ('The Girl on the Train', 'Paula Hawkins', 'A woman becomes entangled in a missing person investigation that reveals dark secrets.'),
    ],
    'Horror': [
        ('The Shining', 'Stephen King', 'A family isolated in a snowbound hotel faces the supernatural forces that drive the father to madness.'),
        ('Dracula', 'Bram Stoker', 'The classic Gothic horror that introduced the most famous vampire in literature.'),
        ('House of Leaves', 'Mark Z. Danielewski', 'A mind-bending tale of a house that is larger on the inside than the outside — a labyrinth of terror.'),
    ],
    'Biography': [
        ('Steve Jobs', 'Walter Isaacson', 'The definitive biography of Apple\'s co-founder based on over forty interviews and extensive research.'),
        ('The Diary of a Young Girl', 'Anne Frank', 'The haunting account of a Jewish girl hiding from Nazis in Amsterdam during World War II.'),
        ('Long Walk to Freedom', 'Nelson Mandela', 'The autobiography of one of the greatest moral leaders of the 20th century.'),
    ],
}

# ── Programmatic title generation to reach 1000 books ──
AUTHORS_FIRST = ['James', 'Robert', 'Michael', 'David', 'Richard', 'William', 'Thomas', 'Daniel',
    'Sarah', 'Emily', 'Jessica', 'Amanda', 'Rachel', 'Laura', 'Rebecca', 'Jennifer',
    'Christopher', 'Andrew', 'Matthew', 'Elizabeth', 'Catherine', 'Margaret', 'Patricia',
    'Jonathan', 'Nicholas', 'Benjamin', 'Victoria', 'Gregory', 'Stephen', 'Alexander']

AUTHORS_LAST = ['Mitchell', 'Harrison', 'Anderson', 'Peterson', 'Collins', 'Richardson',
    'Fletcher', 'Bennett', 'Crawford', 'Sullivan', 'Montgomery', 'Blackwell', 'Whitman',
    'Donovan', 'Sterling', 'Hawthorne', 'Beaumont', 'Kensington', 'Thornton', 'Wellington',
    'Ashford', 'Carrington', 'Ellington', 'Fairchild', 'Gillingham', 'Hollingsworth',
    'Pennington', 'Remington', 'Worthington', 'Langford']

CAT_TITLE_PARTS = {
    'Computer Science': {
        'topics': ['Algorithms', 'Data Structures', 'Machine Learning', 'Cloud Infrastructure', 'Neural Networks',
                   'Computational Complexity', 'Software Verification', 'Parallel Processing', 'Distributed Ledgers',
                   'Quantum Information', 'Compiler Optimization', 'Graph Theory', 'Operating Systems',
                   'Information Retrieval', 'Computer Vision', 'Formal Methods', 'Network Protocols',
                   'Digital Signal Processing', 'Embedded Systems', 'Fault-Tolerant Computing'],
        'subtitles': ['A Modern Approach', 'Theory and Practice', 'Fundamentals and Applications',
                      'An Advanced Perspective', 'From Theory to Implementation', 'Concepts and Techniques',
                      'A Comprehensive Guide', 'Principles and Paradigms', 'Design and Analysis',
                      'Methods and Tools', 'The Complete Reference', 'A Hands-On Introduction'],
    },
    'Programming': {
        'topics': ['Modern Java', 'Advanced Python', 'Rust in Practice', 'TypeScript Design', 'Scala Patterns',
                   'Kotlin Coroutines', 'Swift Protocols', 'Go Concurrency', 'C++ Templates', 'Ruby Metaprogramming',
                   'Functional Programming', 'Reactive Systems', 'Domain-Driven Design', 'API Craftsmanship',
                   'Test-Driven Development', 'Continuous Delivery', 'Microservices Patterns', 'Event Sourcing',
                   'GraphQL APIs', 'WebAssembly Applications'],
        'subtitles': ['Best Practices', 'Hands-On Guide', 'From Beginner to Expert', 'Patterns and Anti-Patterns',
                      'Production-Ready Solutions', 'Real-World Applications', 'The Definitive Guide',
                      'Practical Recipes', 'Enterprise Patterns', 'Clean Architecture', 'Effective Techniques'],
    },
    'Data Science': {
        'topics': ['Statistical Modeling', 'Time Series Forecasting', 'Causal Inference', 'Bayesian Methods',
                   'Dimensionality Reduction', 'Anomaly Detection', 'Experimental Design', 'Survey Analytics',
                   'Spatial Data Analysis', 'Text Analytics', 'Graph Analytics', 'Stream Processing',
                   'Reproducible Research', 'Model Interpretability', 'Forecasting Methods', 'Data Quality'],
        'subtitles': ['with Python', 'A Practical Approach', 'From Data to Decisions', 'Concepts and Case Studies',
                      'Methods and Applications', 'The Complete Toolkit', 'Real-World Analytics',
                      'for Business Intelligence', 'Visualization and Insight', 'Statistical Foundations'],
    },
    'Artificial Intelligence': {
        'topics': ['Transformer Architectures', 'Graph Neural Networks', 'Generative Adversarial Networks',
                   'Multi-Agent Systems', 'Knowledge Graphs', 'Causal Reasoning', 'Transfer Learning',
                   'Federated Learning', 'Self-Supervised Learning', 'Neural Architecture Search',
                   'Explainable AI', 'Robotics Perception', 'Automated Planning', 'Cognitive Architectures',
                   'Bayesian Deep Learning', 'Evolutionary Computation', 'Swarm Intelligence', 'Neuro-Symbolic AI'],
        'subtitles': ['Theory and Applications', 'Modern Approaches', 'From Foundations to Frontiers',
                      'A Comprehensive Introduction', 'Algorithms and Implementations', 'Research and Practice'],
    },
    'Web Development': {
        'topics': ['Full-Stack Applications', 'Progressive Web Apps', 'Serverless Architecture', 'Next.js Projects',
                   'Vue 3 Patterns', 'React Design', 'Angular Architecture', 'Node.js Services',
                   'CSS Architecture', 'Web Performance', 'Accessibility Engineering', 'Cross-Platform Development',
                   'Browser APIs', 'Jamstack Sites', 'Web Security', 'State Management', 'Frontend Testing'],
        'subtitles': ['Modern Patterns', 'Building for Scale', 'A Complete Guide', 'Production Techniques',
                      'Hands-On Projects', 'Architecture and Design', 'from Development to Deployment'],
    },
    'Databases': {
        'topics': ['PostgreSQL Administration', 'Redis Patterns', 'Cassandra at Scale', 'Elasticsearch in Action',
                   'Graph Database Modeling', 'Time-Series Databases', 'Database Migration Strategies',
                   'Query Optimization', 'Data Warehousing', 'Stream Processing with Kafka',
                   'Database Sharding', 'Replication Patterns', 'NoSQL Design', 'SQL Advanced Techniques',
                   'Data Modeling', 'Indexing Strategies', 'Transaction Processing'],
        'subtitles': ['The Complete Reference', 'Design and Optimization', 'Production Guide', 'Architecture Patterns',
                      'Performance Tuning', 'A Practitioner\'s Guide', 'for Modern Applications'],
    },
    'Cybersecurity': {
        'topics': ['Threat Modeling', 'Incident Response', 'Zero Trust Architecture', 'Cloud Security',
                   'Container Security', 'Supply Chain Security', 'Social Engineering Defense', 'Digital Forensics',
                   'Red Team Operations', 'Security Operations', 'Identity and Access Management',
                   'Network Defense', 'Application Security', 'Mobile Security', 'IoT Security'],
        'subtitles': ['A Practitioner\'s Guide', 'Defense in Depth', 'Modern Threats and Defenses',
                      'Hands-On Techniques', 'Strategy and Implementation', 'Risk Assessment and Mitigation'],
    },
    'Mathematics': {
        'topics': ['Abstract Algebra', 'Real Analysis', 'Complex Analysis', 'Topology', 'Number Theory',
                   'Differential Geometry', 'Dynamical Systems', 'Numerical Methods', 'Optimization Theory',
                   'Stochastic Processes', 'Information Geometry', 'Category Theory', 'Graph Theory',
                   'Combinatorial Design', 'Mathematical Logic', 'Fourier Analysis', 'Functional Analysis'],
        'subtitles': ['An Introduction', 'Foundations and Applications', 'Theory and Problems',
                      'A Rigorous Approach', 'Advanced Topics', 'for Scientists and Engineers'],
    },
    'Physics': {
        'topics': ['Quantum Field Theory', 'General Relativity', 'Statistical Mechanics', 'Condensed Matter Physics',
                   'Particle Physics', 'Astrophysics', 'Optics and Photonics', 'Plasma Physics',
                   'Nuclear Physics', 'Solid State Physics', 'Fluid Dynamics', 'Electromagnetic Theory',
                   'Classical Mechanics', 'Thermodynamics', 'Quantum Information', 'Cosmology'],
        'subtitles': ['Principles and Applications', 'A Modern Introduction', 'Theoretical Foundations',
                      'with Experimental Methods', 'for the 21st Century', 'An Advanced Treatment'],
    },
    'History': {
        'topics': ['The Roman Empire', 'Medieval Europe', 'The Renaissance', 'The Age of Exploration',
                   'The Industrial Revolution', 'World War I', 'The Cold War', 'Ancient Civilizations',
                   'The Ottoman Empire', 'Colonial America', 'The French Revolution', 'Imperial China',
                   'The Byzantine Empire', 'The Viking Age', 'The Enlightenment', 'The American Civil War',
                   'The British Empire', 'Japanese History', 'African Kingdoms', 'The Silk Road'],
        'subtitles': ['A New History', 'Power and Society', 'Rise and Fall', 'A Comprehensive Account',
                      'Origins and Legacy', 'People and Events', 'Reconsidered', 'A Narrative History'],
    },
    'Philosophy': {
        'topics': ['Ethics and Morality', 'Political Philosophy', 'Philosophy of Mind', 'Existentialism',
                   'Eastern Philosophy', 'Philosophy of Science', 'Aesthetics', 'Epistemology',
                   'Metaphysics', 'Logic and Reasoning', 'Philosophy of Language', 'Ancient Greek Philosophy',
                   'Buddhist Philosophy', 'Ethics of Technology', 'Freedom and Determinism', 'Consciousness Studies'],
        'subtitles': ['A Very Short Introduction', 'Key Concepts', 'Historical and Contemporary Perspectives',
                      'Arguments and Analysis', 'The Great Debates', 'A Philosophical Investigation'],
    },
    'Psychology': {
        'topics': ['Cognitive Psychology', 'Social Psychology', 'Developmental Psychology', 'Abnormal Psychology',
                   'Positive Psychology', 'Neuropsychology', 'Behavioral Economics', 'Personality Theory',
                   'Emotional Intelligence', 'Attachment Theory', 'Mindfulness and Cognition', 'Trauma and Recovery',
                   'Motivation Science', 'Group Dynamics', 'Child Development', 'Memory and Learning'],
        'subtitles': ['Theory and Research', 'A Scientific Approach', 'Understanding Human Behavior',
                      'Clinical Applications', 'Current Perspectives', 'From Lab to Life'],
    },
    'Self-Help': {
        'topics': ['Personal Growth', 'Emotional Resilience', 'Finding Purpose', 'Mindful Living',
                   'Overcoming Adversity', 'Building Confidence', 'Time Mastery', 'Stress Management',
                   'Better Relationships', 'Creative Living', 'Inner Peace', 'Life Transitions'],
        'subtitles': ['A Practical Guide', 'Transform Your Life', 'The Complete Handbook', 'Simple Strategies',
                      'Evidence-Based Approaches', 'Daily Practices', 'for Modern Life'],
    },
    'Business': {
        'topics': ['Strategic Management', 'Competitive Advantage', 'Business Model Innovation', 'Digital Transformation',
                   'Organizational Culture', 'Change Management', 'Negotiation Strategy', 'Supply Chain Excellence',
                   'Customer Experience', 'Brand Building', 'Corporate Finance', 'Mergers and Acquisitions',
                   'Global Strategy', 'Sustainable Business', 'Family Business', 'Social Enterprise'],
        'subtitles': ['Strategy and Execution', 'A Modern Framework', 'Leading in Times of Change',
                      'Theory and Practice', 'The Essential Guide', 'Building Lasting Value'],
    },
    'Finance': {
        'topics': ['Investment Strategy', 'Portfolio Management', 'Risk Analysis', 'Behavioral Finance',
                   'Financial Modeling', 'Derivatives Markets', 'Fixed Income', 'Alternative Investments',
                   'Private Equity', 'Venture Capital', 'Real Estate Finance', 'Personal Wealth Management',
                   'International Finance', 'FinTech Revolution', 'Quantitative Trading', 'Financial Regulation'],
        'subtitles': ['Principles and Practice', 'A Comprehensive Guide', 'Modern Perspectives',
                      'Analysis and Strategy', 'The Complete Handbook', 'Markets and Instruments'],
    },
    'Economics': {
        'topics': ['Microeconomic Theory', 'Macroeconomic Policy', 'International Trade', 'Development Economics',
                   'Labor Economics', 'Public Finance', 'Monetary Economics', 'Environmental Economics',
                   'Game Theory', 'Industrial Organization', 'Health Economics', 'Urban Economics',
                   'Economic History', 'Inequality and Growth', 'Innovation Economics', 'Behavioral Economics'],
        'subtitles': ['Theory and Evidence', 'A Modern Approach', 'Policy and Practice', 'Global Perspectives',
                      'Principles and Applications', 'Contemporary Debates'],
    },
    'Political Science': {
        'topics': ['Comparative Politics', 'International Relations', 'Democratic Theory', 'Authoritarianism',
                   'Political Economy', 'Public Policy', 'Constitutional Law', 'Electoral Systems',
                   'Political Psychology', 'Social Movements', 'Geopolitics', 'Diplomacy and Statecraft',
                   'Federalism', 'Human Rights', 'Security Studies', 'Environmental Politics'],
        'subtitles': ['A Critical Introduction', 'Theory and Practice', 'Power and Governance',
                      'Contemporary Issues', 'Historical and Comparative Perspectives', 'The Essential Reader'],
    },
    'Science': {
        'topics': ['Evolutionary Biology', 'Genetics and Genomics', 'Neuroscience', 'Climate Science',
                   'Marine Biology', 'Microbiology', 'Ecology', 'Biochemistry', 'Astronomy',
                   'Paleontology', 'Botany', 'Zoology', 'Geology', 'Meteorology', 'Oceanography',
                   'Anthropology', 'Archaeology', 'Virology', 'Immunology', 'Pharmacology'],
        'subtitles': ['A Popular Guide', 'Discoveries and Insights', 'The Science of', 'Exploring',
                      'Understanding', 'Frontiers of', 'An Illustrated Introduction to'],
    },
    'Fiction': {
        'topics': ['The Last Letter', 'Small Town Shadows', 'The Garden of Memories', 'Crossing the Bridge',
                   'Beneath the Surface', 'The Glass House', 'Thirteen Winters', 'After the Rain',
                   'The Inheritance', 'Voices in the Dark', 'The Copper Beech', 'The Passenger',
                   'Inheritance of Loss', 'The Night Watch', 'A Perfect Stranger', 'The Stone Garden',
                   'Half a World Away', 'The Forgotten Room', 'Burning Bridges', 'The Silent Patient'],
        'subtitles': ['A Novel', '', 'Stories', '', 'A Novel', '', '', '', 'A Novel', ''],
    },
    'Science Fiction': {
        'topics': ['The Last Colony', 'Starfall', 'Quantum Drift', 'The Exodus Protocol', 'Machine Dawn',
                   'The Echo Chamber', 'Orbital Decay', 'The Genesis Machine', 'Dark Matter Rising',
                   'The Turing Test', 'Event Horizon', 'The Signal', 'Post-Human',
                   'The Colony Ship', 'Chronos Gate', 'The Void Between', 'Silicon Soul', 'Red Planet Rising'],
        'subtitles': ['A Novel', '', '', 'Book One', '', 'The Series', '', 'A Novel'],
    },
    'Fantasy': {
        'topics': ['The Last Dragon Lord', 'Shadow and Bone', 'The Iron Crown', 'The Silver Throne',
                   'A Court of Thorns', 'The Obsidian Blade', 'The Dream Weaver', 'The Bone Witch',
                   'Kingdoms of Ash', 'The Crystal Mage', 'The Storm King', 'The Ember Throne',
                   'The Raven Queen', 'Sword of Destiny', 'The Wolf King', 'The Midnight Court'],
        'subtitles': ['Book One', 'A Novel', '', 'The Chronicles', 'Book One', '', 'A Novel', ''],
    },
    'Mystery': {
        'topics': ['The Missing Heiress', 'Death at Midnight', 'The Locked Room', 'The Dead Witness',
                   'Murder at the Manor', 'The Final Alibi', 'The Vanishing Act', 'The Silent Detective',
                   'The Poison Pen', 'A Body in the Library', 'The Cold Trail', 'The Fourth Suspect',
                   'Death on the River', 'The Perfect Alibi', 'The Lost Evidence', 'The Foggy Night'],
        'subtitles': ['A Detective Novel', 'A Mystery', '', '', 'A Crime Novel', '', '', 'A Thriller'],
    },
    'Romance': {
        'topics': ['A Summer in Provence', 'Love in the City', 'The Wedding Date', 'The Long Way Home',
                   'Hearts on Fire', 'The Second Chance', 'Under the Tuscan Moon', 'A Winter Wedding',
                   'The Love Letter', 'Meet Me at Sunset', 'The Beach House', 'Love Unexpected',
                   'The Promise Ring', 'Forever Begins Today', 'The Last First Kiss', 'Love in Translation'],
        'subtitles': ['A Romance', '', '', 'A Love Story', '', '', '', ''],
    },
    'Thriller': {
        'topics': ['The Asset', 'Dead Drop', 'The Operative', 'False Flag', 'The Extraction',
                   'The Conspiracy', 'Safe House', 'The Double Agent', 'Rendition', 'The Informant',
                   'The Intercept', 'Zero Hour', 'The Breach', 'Sleeper Cell', 'The Kill Chain',
                   'Treason', 'The Handler', 'Clean Sweep', 'The Defector', 'Burning Ground'],
        'subtitles': ['A Thriller', '', '', 'A Novel', '', '', 'A Spy Thriller', ''],
    },
    'Horror': {
        'topics': ['The Haunting of Blackwood Manor', 'The Whispering Dark', 'The Devil\'s Hour', 'The Hollow',
                   'The Cursed', 'Shadow over Innsmouth', 'The Wendigo', 'The Last Séance',
                   'The Dead of Winter', 'The Possession', 'The Graveyard Shift', 'The Skinwalker',
                   'The Nightmare', 'The Blood Ritual', 'The Abyss', 'The Witching Hour'],
        'subtitles': ['A Horror Novel', '', '', '', 'A Supernatural Thriller', '', '', ''],
    },
    'Biography': {
        'topics': ['Elon Musk', 'Marie Curie', 'Leonardo da Vinci', 'Frida Kahlo', 'Winston Churchill',
                   'Ada Lovelace', 'Alan Turing', 'Mahatma Gandhi', 'Harriet Tubman', 'Albert Einstein',
                   'Florence Nightingale', 'Abraham Lincoln', 'Cleopatra', 'Genghis Khan',
                   'Catherine the Great', 'Martin Luther King Jr.', 'Charles Darwin', 'Joan of Arc'],
        'subtitles': ['A Biography', 'The Life and Times', 'A Life', 'The Definitive Biography',
                      'A Life in Full', 'Legacy', 'Genius and Tragedy', 'The Untold Story'],
    },
}

# ── Categories ──
CATEGORIES = list(TITLE_POOLS.keys())

# ── Generator helpers ──
def _gen_title(cat_name):
    parts = CAT_TITLE_PARTS.get(cat_name, CAT_TITLE_PARTS['Fiction'])
    if isinstance(parts, list):
        parts = parts[0]
    topic = random.choice(parts['topics'])
    subtitle = random.choice(parts['subtitles'])
    if subtitle and random.random() > 0.4:
        return f'{topic}: {subtitle}'
    return topic

def _gen_author():
    return f'{random.choice(AUTHORS_FIRST)} {random.choice(AUTHORS_LAST)}'

def _gen_description(title):
    prefixes = ['This book explores', 'A comprehensive examination of', 'An insightful look at',
                'A groundbreaking study of', 'This work investigates', 'This volume presents',
                'An authoritative guide to', 'A thought-provoking analysis of']
    t = title.lower().replace(':', '').replace('  ', ' ').strip()
    return (f'{random.choice(prefixes)} {t}. '
            f'{"Packed with practical examples and theoretical depth" if random.random() > 0.5 else "Drawing on extensive research and real-world applications"}. '
            f'{"Essential reading for anyone interested in this field." if random.random() > 0.5 else "A valuable resource for students and practitioners alike."}')

# ── Bot names ──
BOT_NAMES = [
    'Alex Johnson', 'Morgan Williams', 'Taylor Brown', 'Jordan Davis', 'Casey Miller',
    'Riley Wilson', 'Quinn Anderson', 'Avery Thomas', 'Skyler Martinez', 'Harper Robinson',
    'Dakota Clark', 'Reese Lewis', 'Finley Walker', 'Rowan Hall', 'Emerson Young',
    'Blake King', 'Cameron Wright', 'Sage Lopez', 'Phoenix Hill', 'Drew Scott',
    'Jamie Green', 'Kendall Adams', 'Aubrey Baker', 'Charlie Nelson', 'Shane Carter',
    'River Mitchell', 'Hayden Roberts', 'Lane Turner', 'Ellis Phillips', 'Devon Campbell',
    'Jules Parker', 'Quinn Evans', 'Remi Edwards', 'Wren Collins', 'Asher Stewart',
    'Sloane Morris', 'Dakota Rogers', 'Tatum Reed', 'Sage Cook', 'Reece Morgan',
    'Tory Bell', 'Pat Murphy', 'Chris Cooper', 'Jesse Bailey', 'Frankie Howard',
    'Stevie Ward', 'Billie Torres', 'Marion Peterson', 'Leslie Gray', 'Robin James',
]

# ── Review templates ──
REVIEWS = [
    'An absolute masterpiece. Could not put it down!',
    'Really well written and thoroughly researched. Highly recommended.',
    'Decent read but could have been more concise in some parts.',
    'One of the best books I have ever read. Truly life-changing.',
    'The writing style is engaging and the content is practical.',
    'A bit dry at times but the information is invaluable.',
    'Perfect blend of theory and real-world examples.',
    'Not what I expected, but pleasantly surprised by the depth.',
    'The author really knows the subject matter. Excellent reference.',
    'Read this in one sitting. Captivating from start to finish.',
    'Good introduction to the topic, but lacking advanced coverage.',
    'Well-structured and easy to follow. Great for beginners.',
    'The examples are outdated but the core concepts remain solid.',
    'A must-read for anyone serious about this field.',
    'Beautifully written with profound insights on every page.',
    'Practical advice that I have already started applying.',
    'Overhyped. The content is good but not revolutionary.',
    'Clear, concise, and to the point. Exactly what I needed.',
    'The narrative is compelling and the characters are unforgettable.',
    'Solid reference book. I keep coming back to it.',
    'Could have been half the length without losing anything.',
    'Excellent compilation of wisdom from multiple disciplines.',
    'The prose is beautiful. A joy to read slowly.',
    'Very technical but explained in an accessible way.',
    'Falls short of expectations. The premise is better than the execution.',
    'A game-changer. Completely shifted my perspective.',
    'Entertaining and educational — a rare combination.',
    'Dense but rewarding. Take your time with this one.',
    'The author makes complex topics feel simple and intuitive.',
    'A solid 4 stars. Good content, well organized, occasionally repetitive.',
]


class Command(BaseCommand):
    help = 'Seed database with admin/demo users, categories, 1000 books, 50 bot users, and ratings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # ── 1. Users ──
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@ebook.com', 'role': 'admin', 'is_superuser': True, 'is_staff': True}
        )
        if not admin.is_superuser:
            admin.is_superuser = True; admin.is_staff = True; admin.role = 'admin'; admin.save()
            self.stdout.write('Fixed admin permissions')
        else:
            self.stdout.write('Admin user ready (admin / admin123)')

        demo, _ = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@ebook.com', 'role': 'user'}
        )
        demo.set_password('demo123'); demo.save()
        self.stdout.write('Demo user ready (demo / demo123)')

        # ── 2. Categories ──
        from books.models import Category
        cat_objs = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name)
            cat_objs[name] = cat
        self.stdout.write(f'Categories: {len(cat_objs)}')

        # ── 3. Books ──
        from books.models import Book, BookStats
        existing = Book.objects.count()
        count = 0

        for cat_name, entries in TITLE_POOLS.items():
            for title, author, desc in entries:
                book, created = Book.objects.get_or_create(
                    title=title,
                    defaults={
                        'author': author,
                        'description': desc,
                        'category': cat_objs[cat_name],
                        'price': round(random.uniform(4.99, 59.99), 2),
                        'cover_url': f'https://picsum.photos/seed/book{hash(title) % 10000}/200/300',
                        'download_url': f'https://example.com/downloads/{hash(title) % 10000}',
                        'tags': f'{cat_name.lower()}, {random.choice(["bestseller","classic","new release","popular","recommended","award-winning"])}',
                        'publish_date': f'20{random.randint(0, 24):02d}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                    }
                )
                if created:
                    stats = BookStats.objects.create(book=book)
                    stats.view_count = random.randint(20, 8000)
                    stats.favorite_count = random.randint(2, 600)
                    stats.purchase_count = random.randint(5, 400)
                    stats.download_count = random.randint(3, 300)
                    stats.calculate_hot_score()
                    count += 1

        # ── 3b. Programmatic book generation to reach 1000 ──
        TARGET = 1000
        current = Book.objects.count()
        needed = TARGET - current
        gen_count = 0
        if needed > 0:
            self.stdout.write(f'Generating {needed} more books...')
            gen_count = 0
            seen_titles = set(Book.objects.values_list('title', flat=True))
            attempts = 0
            while gen_count < needed and attempts < needed * 5:
                attempts += 1
                cat_name = random.choice(CATEGORIES)
                title = _gen_title(cat_name)
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                author = _gen_author()
                desc = _gen_description(title)
                try:
                    book = Book.objects.create(
                        title=title,
                        author=author,
                        description=desc,
                        category=cat_objs[cat_name],
                        price=round(random.uniform(4.99, 59.99), 2),
                        cover_url=f'https://picsum.photos/seed/book{hash(title) % 100000}/200/300',
                        download_url=f'https://example.com/downloads/{hash(title) % 100000}',
                        tags=f'{cat_name.lower()}, {random.choice(["bestseller","classic","new release","popular","recommended","award-winning"])}',
                        publish_date=f'20{random.randint(0, 24):02d}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                    )
                    stats = BookStats.objects.create(book=book)
                    stats.view_count = random.randint(20, 8000)
                    stats.favorite_count = random.randint(2, 600)
                    stats.purchase_count = random.randint(5, 400)
                    stats.download_count = random.randint(3, 300)
                    stats.calculate_hot_score()
                    gen_count += 1
                except Exception:
                    pass

        self.stdout.write(f'Books: {Book.objects.count()} (added {count} curated + {gen_count} generated)')

        # ── 4. Bot users ──
        bots_created = 0
        bot_users = []
        for name in BOT_NAMES:
            username = name.lower().replace(' ', '_')
            bot, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@ebook.com', 'role': 'user'}
            )
            if created:
                bot.set_password('password123')
                bot.save()
                bots_created += 1
            bot_users.append(bot)
        self.stdout.write(f'Bot users created: {bots_created} (total: {len(bot_users)})')

        # ── 5. Ratings & reviews from bots ──
        from ratings.models import Rating
        all_books = list(Book.objects.all())
        ratings_created = 0

        for bot in bot_users:
            # Each bot rates 10-30 random books
            num = random.randint(10, 30)
            rated_books = random.sample(all_books, min(num, len(all_books)))
            for book in rated_books:
                _, created = Rating.objects.get_or_create(
                    user=bot, book=book,
                    defaults={
                        'rating': random.randint(3, 5),
                        'review': random.choice(REVIEWS),
                    }
                )
                if created:
                    ratings_created += 1

        self.stdout.write(f'Ratings/reviews created: {ratings_created}')

        # ── 6. Demo user also rates some books ──
        for book in random.sample(all_books, min(15, len(all_books))):
            Rating.objects.get_or_create(
                user=demo, book=book,
                defaults={'rating': random.randint(3, 5), 'review': random.choice(REVIEWS)}
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete! {Book.objects.count()} books, {Category.objects.count()} categories, '
            f'{User.objects.filter(role="user").count()} users, '
            f'{Rating.objects.count()} ratings'
        ))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Demo: demo / demo123')
        self.stdout.write('Bot accounts: bot_name / password123')
