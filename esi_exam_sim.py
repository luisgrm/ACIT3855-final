import random

# --- FULL DATASET: QUIZZES 1-11 ---
QUIZ_DATA = [
    # --- QUIZ 1 ---
    {"q": "Define Enterprise. Select the best answer.", "type": "s", "o": ["Business or Company", "Large Business Only", "Small Business Only", "A Startup Company"], "a": ["Business or Company"]},
    {"q": "Which are examples of an Enterprise System. Select all that would apply.", "type": "m", "o": ["A script used by a software developer to track productivity", "Source code management system used by multiple software development teams", "Time tracking system that all employees use to fill out a weekly timesheet", "Web based Customer Relationship Management (CRM) system", "System for managing the personal information of employees (HR)", "Knowledge Base tool used by the software development teams to collaborate", "Excel Spreadsheet used by an individual salesperson"], "a": ["Source code management system used by multiple software development teams", "Time tracking system that all employees use to fill out a weekly timesheet", "Web based Customer Relationship Management (CRM) system", "System for managing the personal information of employees (HR)", "Knowledge Base tool used by the software development teams to collaborate"]},
    {"q": "In which scenario below would using Cloud Based Software (i.e., SaaS) likely be most advantageous?", "type": "s", "o": ["You are a small company with limited IT resources", "You are storing sensitive data (i.e., trade secrets)", "You already have on-premise infrastructure", "Your IT department has specific security requirements"], "a": ["You are a small company with limited IT resources"]},
    {"q": "In which scenario below would deploying software to On-Premise Infrastructure likely be most advantageous? Select all that apply.", "type": "m", "o": ["You are storing sensitive data (i.e., trade secrets)", "You are a small company with limited IT resources", "You already have On-Premise Infrastructure", "Your IT department has specific security requirements", "You are prototyping new software applications with auto-scaling"], "a": ["You are storing sensitive data (i.e., trade secrets)", "You already have On-Premise Infrastructure", "Your IT department has specific security requirements"]},
    {"q": "Identify three areas where you would want to compare BitBucket, GitHub and GitLab.", "type": "m", "o": ["Integration with other tools", "Security and access control", "Features and workflow support", "Price of the coffee in the office"], "a": ["Integration with other tools", "Security and access control", "Features and workflow support"]},
    {"q": "Which installation methods do you have for a production installation of Confluence or JIRA?", "type": "m", "o": ["Installer - Windows", "Zip or Archive File", "Docker Container", "Installer - Linux", "Cluster (High-Availability)", "Installer - Mac"], "a": ["Installer - Windows", "Installer - Linux", "Cluster (High-Availability)"]},
    {"q": "What capability does Confluence provide?", "type": "s", "o": ["Work Management", "Database", "Knowledge Base", "Source Code Management"], "a": ["Knowledge Base"]},
    {"q": "What capability does JIRA provide?", "type": "s", "o": ["Source Code Management", "Database", "Work Management", "Knowledge Base"], "a": ["Work Management"]},

    # --- QUIZ 2 ---
    {"q": "Select the best definition of a Functional Requirement.", "type": "s", "o": ["Defines a function of a system or its component", "Defines function points in the software", "Defines how the software source code functions", "Defines a function in a procedural program"], "a": ["Defines a function of a system or its component"]},
    {"q": "Select the best definition of a Non-Functional Requirement.", "type": "s", "o": ["Defines constraints on the design or implementation of a system", "Defines all code defined outside of functions", "Defines the infrastructure needed to support the Functional Requirements", "Defines the design of the software source code"], "a": ["Defines constraints on the design or implementation of a system"]},
    {"q": "Which of the following are examples of Functional Requirement(s)?", "type": "s", "o": ["The system should bill the user's credit card immediately after order confirmation", "All data with PII stored in the database should be encrypted", "The system should fail over to backup within 20 minutes", "The system should be capable of being restored from backups within 8 hours"], "a": ["The system should bill the user's credit card immediately after order confirmation"]},
    {"q": "For Functional Requirements, a function is described as a specification of behavior between outputs and inputs", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Functional requirements may involve calculations, technical details, data manipulation and processing.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Which of the following are categories of Non-Functional Requirements? Select all that apply.", "type": "m", "o": ["Security", "Scalability", "Availability", "Usability", "Testability", "Maintainability"], "a": ["Security", "Scalability", "Availability", "Usability", "Testability", "Maintainability"]},
    {"q": "Non-Functional Requirements are also referred to as Architecturally Significant Requirements.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Non-Functional Requirements are also referred to as 'ilities'.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Non-Functional Requirements are also referred to as System Quality Attributes.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Which of the following would be considered examples of Non-Functional Requirement(s)?", "type": "m", "o": ["A web application should be capable enough to handle 2 million concurrent users", "A web application should provide e-mail notification when an order completes", "A web application should allow users to enter orders", "A web application should work on the Chrome, Firefox and Safari browsers"], "a": ["A web application should be capable enough to handle 2 million concurrent users", "A web application should work on the Chrome, Firefox and Safari browsers"]},

    # --- QUIZ 3 ---
    {"q": "DevOps is the practice of operations and development engineers participating together in the entire service lifecycle.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Identify the three primary practice areas of DevOps.", "type": "m", "o": ["Site Reliability Engineering", "Infrastructure Automation", "On-Call Developers", "Continuous Delivery", "Agile Practices", "DevOps Practices"], "a": ["Site Reliability Engineering", "Infrastructure Automation", "Continuous Delivery"]},
    {"q": "Infrastructure Automation refers to creating your systems, OS configs, and app deployments as code.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Continuous Delivery means having developers and operations engineers manually build, test, deploy your apps daily.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "Site Reliability Engineering includes operating your systems; monitoring and orchestration.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "What should go in your project's single source code repository?", "type": "m", "o": ["Operating System", "Database Schema", "Code", "Test Scripts", "Install Scripts", "Binaries compiled from your source code"], "a": ["Database Schema", "Code", "Test Scripts", "Install Scripts"]},
    {"q": "A continuous integration server is where (select the best answer):", "type": "s", "o": ["The build is run manually on a daily basis", "The build is run automatically on a daily basis", "The build is run automatically every time the code changes", "The build is run automatically every 5 minutes"], "a": ["The build is run automatically every time the code changes"]},
    {"q": "Frequently committing to the mainline helps developers quickly find out if there's a conflict.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "When a build breaks, 'nobody has a higher priority task than fixing the build'. This means all developers must focus on it.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "Important characteristics of a good CI pipeline?", "type": "m", "o": ["Automated Build", "Fast Build and Test", "Automated Tests", "Visibility", "Manual Processes", "Runs on Every Checkin"], "a": ["Automated Build", "Fast Build and Test", "Automated Tests", "Visibility", "Runs on Every Checkin"]},
    {"q": "A stakeholder is anyone that has an interest (or concern) in the realization of the system.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Who would most likely be considered stakeholders for our Enterprise Development Environment?", "type": "m", "o": ["HR Manager", "Office Receptionist", "IT Operations Team", "Test Team", "Development Team", "Project Manager"], "a": ["IT Operations Team", "Test Team", "Development Team", "Project Manager"]},

    # --- QUIZ 4 ---
    {"q": "The definition of a Jenkins pipeline is written in a text file called?", "type": "s", "o": ["Pipelinefile", "Jenkinsfile", "Definitionfile", "Textfile"], "a": ["Jenkinsfile"]},
    {"q": "Advantages of defining a Jenkins pipeline in source control?", "type": "m", "o": ["Code review/iteration", "Single source of truth", "Audit trail", "Full automation (no human intervention)", "Can be setup to automatically create a Pipeline build process for all branches"], "a": ["Code review/iteration", "Single source of truth", "Audit trail", "Can be setup to automatically create a Pipeline build process for all branches"]},
    {"q": "A Pipeline is a user-defined model of a CI/CD pipeline.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "In Jenkins declarative pipeline syntax, the pipeline is organized into the following:", "type": "s", "o": ["jenkins block", "main function", "node block", "pipeline block containing stages"], "a": ["pipeline block containing stages"]},
    {"q": "A stage block defines a conceptually distinct subset of tasks performed by the Pipeline", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "The agent section of a declarative pipeline definition has which characteristics (Select 3):", "type": "m", "o": ["Required", "Specifies where the pipeline will execute", "Can specify a docker image", "Validates the outputs"], "a": ["Required", "Specifies where the pipeline will execute", "Can specify a docker image"]},
    {"q": "A Jenkins pipeline should be triggered by which of the following?", "type": "s", "o": ["Fixed Schedule", "Buildmaster", "Manually", "Change to the Source Code"], "a": ["Change to the Source Code"]},
    {"q": "It is generally considered best practice to maintain the Jenkins pipeline definition directly within a Jenkins build job", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "A Step in a Jenkins pipeline is a single task. Fundamentally, a step tells Jenkins what to do.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Jenkins pipelines support parallel execution and definition of shared libraries.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "The Jenkins web server and 'brains' of the system. Select the best answer.", "type": "s", "o": ["Executor", "Builtin Node", "Controller", "Agent"], "a": ["Controller"]},
    {"q": "Manages the execution of tasks on a node. Select the best answer.", "type": "s", "o": ["Builtin Node", "Agent", "Executor", "Controller"], "a": ["Agent"]},
    {"q": "Runs the stages in a pipeline. Select the best answer.", "type": "s", "o": ["Controller", "Builtin Node", "Agent", "Executor"], "a": ["Executor"]},
    {"q": "An Agent is a Java application that connects to the Controller and is meant to be highly reliable.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "An Agent and a Node are effectively the same thing", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Identify 2 key reasons for using Jenkins Agent Nodes that are separate from the Jenkins Controller.", "type": "m", "o": ["Cross Browser Support", "Interoperability", "Cross Platform Support", "Scalability", "Simpler Setup", "Security"], "a": ["Cross Platform Support", "Scalability"]},

    # --- QUIZ 5 ---
    {"q": "In Jenkins pipeline, a shared library consists of which three items?", "type": "m", "o": ["DRY", "Jenkinsfile", "Version", "Source Code Retrieval Method", "Name"], "a": ["Version", "Source Code Retrieval Method", "Name"]},
    {"q": "Shared Libraries in Jenkins pipelines let us share parts of Pipelines to keep code 'DRY'.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Shared libraries for Jenkins pipelines can include code written in which language?", "type": "s", "o": ["Java", "Python", "Groovy", "Ruby"], "a": ["Groovy"]},
    {"q": "Given the shared library vars/evenOrOdd.groovy, how would you import and call the code:", "type": "s", "o": ["@Library('my-shared-library') _ \nmy-shared-library.call(currentBuild.getNumber())", "@Library('my-shared-library') \nevenOrOdd(currentBuild.getNumber())", "@Library('my-shared-library') _ \nevenOrOdd(currentBuild.getNumber())", "@Library('my-shared-library') _ \nmy-shared-library.evenOrOdd(currentBuild.getNumber())"], "a": ["@Library('my-shared-library') _ \nevenOrOdd(currentBuild.getNumber())"]},
    {"q": "A Shared Library Repository is organized into: /src (Groovy), /vars (variables), /resources (non-Groovy).", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Select the tools available for development of Jenkins Pipelines (Select 4):", "type": "m", "o": ["Blue Ocean Editor", "Microsoft Word", "Jenkinsfile IDE", "IDE Plugin", "Command-Line Pipeline Linter", "Replay Pipeline Runs with Modifications"], "a": ["Blue Ocean Editor", "IDE Plugin", "Command-Line Pipeline Linter", "Replay Pipeline Runs with Modifications"]},
    {"q": "In Lab 5 Python program pipeline, what were the stages?", "type": "s", "o": ["Requirements, Unit Test, Deploy", "Build, Unit Test, Integration Test", "Build, Unit Test, Deploy", "Requirements, Unit Test, Integration Test"], "a": ["Build, Unit Test, Deploy"]},
    {"q": "Why would we want to use shared libraries for Jenkins pipelines?", "type": "m", "o": ["Code Reuse", "Complexity", "Code Quality", "Code Structure"], "a": ["Code Reuse", "Code Quality", "Code Structure"]},
    {"q": "Global Pipeline Libraries are only available to specific pipeline jobs.", "type": "s", "o": ["True", "False"], "a": ["False"]},

    # --- QUIZ 6 ---
    {"q": "Static code analysis is best described as...", "type": "s", "o": ["Inspection of code during execution", "Automated inspection of code", "Inspection of code without execution", "Visual inspection of code"], "a": ["Inspection of code without execution"]},
    {"q": "Three benefits of static code analysis include:", "type": "m", "o": ["Automated tools can find errors without running the program", "Finds errors that only occur when run", "Reveal errors that manifest months after release", "Reduce manual code review effort", "Ensure code complies with industry standards"], "a": ["Reveal errors that manifest months after release", "Reduce manual code review effort", "Ensure code complies with industry standards"]},
    {"q": "Static and dynamic code analysis together are referred to as:", "type": "s", "o": ["White box testing", "Red box testing", "Black box testing", "Glass box testing"], "a": ["Glass box testing"]},
    {"q": "You should not set and enforce a quality gate until all code, new and old, will meet the standard.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "What are the types of issues that SonarQube can track in your code?", "type": "m", "o": ["Change Requests", "Code Smells", "Vulnerabilities", "Errors", "Warnings", "Bugs"], "a": ["Code Smells", "Vulnerabilities", "Bugs"]},
    {"q": "SonarQube's definition of Technical Debt: The estimated time required to fix maintainability issues and code smells.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "In SonarQube, a snapshot is a set of measures and issues on a given project at a given time.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "In SonarQube, what best describes a scanner?", "type": "s", "o": ["Analysis of code quality", "Stores configuration", "Web interface", "A client application that analyzes the source code to compute snapshots."], "a": ["A client application that analyzes the source code to compute snapshots."]},
    {"q": "What are the four main components of the SonarQube platform?", "type": "m", "o": ["Server (Web, Search, Compute Engine)", "Cluster", "REST API", "Database", "Plugins", "Scanners for Code Analysis"], "a": ["Server (Web, Search, Compute Engine)", "Database", "Plugins", "Scanners for Code Analysis"]},
    {"q": "Where should code analysis first be performed using the SonarQube platform?", "type": "s", "o": ["SonarQube Server", "SonarLint in the IDE", "Source Code Management", "SonarScanner"], "a": ["SonarLint in the IDE"]},

    # --- QUIZ 7 ---
    {"q": "The agents that run your jobs in GitLab CI", "type": "s", "o": ["Pipelines", "CI/CD Components", "CI/CD Variables", "Runners"], "a": ["Runners"]},
    {"q": "Made up of jobs and stages in GitLab CI", "type": "s", "o": ["Pipelines", "CI/CD Variables", "Runners", "CI/CD Components"], "a": ["Pipelines"]},
    {"q": "A way to store values you want to re-use in a GitLab CI pipeline", "type": "s", "o": ["Runners", "CI/CD Variables", "CI/CD Components", "Pipelines"], "a": ["CI/CD Variables"]},
    {"q": "A reusable single pipeline configuration unit in GitLab CI", "type": "s", "o": ["Pipelines", "Runners", "CI/CD Components", "CI/CD Variables"], "a": ["CI/CD Components"]},
    {"q": "A GitLab runner is effectively equivalent to a Jenkins agent node.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Self-managed runners are hosted on your own infrastructure", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "SaaS runners are managed by GitLab and fully integrated with GitLab.com.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "A GitLab runner with a Shell executor has access to all the dependencies installed on the machine.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "In a pipeline defined in a gitlab-ci.yml file, each stage belongs to a job", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "The closest equivalent to a Jenkinsfile pipeline steps block in a gitlab-ci.yml is...", "type": "s", "o": ["environment", "stage", "script", "job"], "a": ["script"]},

    # --- QUIZ 8 ---
    {"q": "Identify two key characteristics of an artifact repository.", "type": "m", "o": ["Artifacts are version controlled", "Artifacts are shared", "Artifacts are merged", "Artifacts are compressed"], "a": ["Artifacts are version controlled", "Artifacts are shared"]},
    {"q": "What advantage does an artifact repository have over storing artifacts as plain files on a shared filesystem?", "type": "s", "o": ["Artifacts are versioned", "Artifacts are compressed", "Artifacts are backed up", "Artifacts are tagged with keywords"], "a": ["Artifacts are versioned"]},
    {"q": "Why would you use an Artifact Management tool rather than your SCM tool (Git)?", "type": "s", "o": ["Cheaper cost", "More tools are better", "Avoid bloating your source code repositories with large files", "Easier integration into CI pipelines"], "a": ["Avoid bloating your source code repositories with large files"]},
    {"q": "In addition to Sonatype Nexus, what are some other artifact management tools (Select 3)?", "type": "m", "o": ["GitHub", "Archiva", "Artifactory", "Maven Artifact Repository", "Bitbucket"], "a": ["Archiva", "Artifactory", "Maven Artifact Repository"]},
    {"q": "What are the advantages of storing 3rd party artifacts internally (Select 3)?", "type": "m", "o": ["Reduced use of 3rd party artifacts", "Insulate company from internet outages", "Reduce network bandwidth", "Faster build times", "Increased collaboration"], "a": ["Insulate company from internet outages", "Reduce network bandwidth", "Faster build times"]},
    {"q": "A component is a library or framework used at runtime, integration or unit test execution.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "A component can even be an entire software application. Docker images are examples of components.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Examples of typical component formats for dependencies include (Select all):", "type": "m", "o": ["Docker Images", "Zip or .tar.gz Files", "Java JAR, WAR, EAR Formats", "RubyGem", "Word Documents", "JSON Files"], "a": ["Docker Images", "Zip or .tar.gz Files", "Java JAR, WAR, EAR Formats", "RubyGem"]},
    {"q": "Which are examples of public repositories?", "type": "m", "o": ["Docker Hub", "Google Docs", "Stack Overflow", "Maven Central Repository"], "a": ["Docker Hub", "Maven Central Repository"]},
    {"q": "A Repository Manager manages access to all public repositories and internal software components.", "type": "s", "o": ["True", "False"], "a": ["True"]},

    # --- QUIZ 9 ---
    {"q": "When we deploy software more frequently, we must accept lower levels of stability and reliability.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "Identify three benefits of adopting Continuous Delivery practices.", "type": "m", "o": ["Higher quality", "Low risk releases", "Lower costs", "Higher revenues", "Fewer developers needed"], "a": ["Higher quality", "Low risk releases", "Lower costs"]},
    {"q": "Match CD Principle: 'Everyone is responsible'. In high performing organizations...", "type": "s", "o": ["Nothing is 'somebody else's problem'", "Work in small batches", "Computers perform repetitive tasks"], "a": ["Nothing is 'somebody else's problem'"]},
    {"q": "What are two overriding goals of Configuration Management?", "type": "m", "o": ["Reproducibility", "Traceability", "Disaster Recovery", "Higher Quality", "Lower Costs"], "a": ["Reproducibility", "Traceability"]},
    {"q": "Continuous integration was invented to address painful integration of long-lived branches.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Continuous Testing can best be defined as...", "type": "s", "o": ["Running unit tests", "Running tests continually throughout the delivery process", "Developers testing as they code", "Manual testing at every stage"], "a": ["Running tests continually throughout the delivery process"]},
    {"q": "In the deployment pipeline pattern, every change runs a build that does (Select 4):", "type": "m", "o": ["Creates packages", "Allows self-service deployment", "Waits for testers to manually verify", "Runs unit tests", "Runs additional tests on packages"], "a": ["Creates packages", "Allows self-service deployment", "Runs unit tests", "Runs additional tests on packages"]},
    {"q": "In the deployment pipeline, every change is effectively a release candidate.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Docker enables which three use cases?", "type": "m", "o": ["Keeping DevOps Engineers employed", "Responsive deployment and scaling", "Running more workloads on the same hardware", "Fast, consistent delivery of your applications"], "a": ["Responsive deployment and scaling", "Running more workloads on the same hardware", "Fast, consistent delivery of your applications"]},
    {"q": "Docker Compose allows you to start and stop multiple Docker containers with single commands.", "type": "s", "o": ["True", "False"], "a": ["True"]},

    # --- QUIZ 10 ---
    {"q": "In Trunk-based development, developers and release engineers only branch when it is absolutely necessary.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "What are three benefits of using Trunk-Based development?", "type": "m", "o": ["Eliminates unnecessary divergence", "Helps minimize merge conflicts", "Manage large-scale projects", "Enables developers to move fast", "Tight control over junior developers"], "a": ["Eliminates unnecessary divergence", "Helps minimize merge conflicts", "Enables developers to move fast"]},
    {"q": "What two scenarios below would be best for Trunk-Based Development?", "type": "m", "o": ["Big team with variety of skill levels", "Software is mission critical", "Experienced team that needs less oversight", "Pushing out a new product fast"], "a": ["Experienced team that needs less oversight", "Pushing out a new product fast"]},
    {"q": "Feature driven development breaks up branches based on the features in a product.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "What are two benefits of using Feature Branching?", "type": "m", "o": ["Tight control over junior/outsourced teams", "Move fast (no merge steps)", "Can more easily manage large-scale projects", "Minimize merge conflicts"], "a": ["Tight control over junior/outsourced teams", "Can more easily manage large-scale projects"]},
    {"q": "Feature Branching is most closely associated with the following Git workflow:", "type": "s", "o": ["Centralized Repository", "Forking", "Merge Requests", "Pull Requests", "Gitflow"], "a": ["Gitflow"]},
    {"q": "What two scenarios below would be best for Feature Branching?", "type": "m", "o": ["Pushing out a new product fast", "Experienced team", "Big team variety of skill levels", "Software is mission critical"], "a": ["Big team variety of skill levels", "Software is mission critical"]},
    {"q": "Pull requests let you tell others about changes on branch in GitLab.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "A Merge Request (MR) is the basis of GitHub as a code collaboration platform.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "How can you use a merge/pull request to improve the quality of your code? (Select 3)", "type": "m", "o": ["Merge changes directly to master", "Require team lead approval before merging", "Get feedback from collaborators", "Run a CI pipeline on proposed changes"], "a": ["Require team lead approval before merging", "Get feedback from collaborators", "Run a CI pipeline on proposed changes"]},

    # --- QUIZ 11 ---
    {"q": "Identify two ways to deal with variables containing sensitive info in GitLab CI:", "type": "m", "o": ["Mask the variable", "Use external password manager", "Tag with 'secret'", "Use hard to guess passwords"], "a": ["Mask the variable", "Use external password manager"]},
    {"q": "Pre-Defined CI/CD variables are those that you as a pipeline developer define in advance.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "UI CI/CD variables in GitLab CI are equivalent to what in Jenkins?", "type": "s", "o": ["Groovy function parameters", "when expression", "agent", "pipeline parameters"], "a": ["pipeline parameters"]},
    {"q": "It is safe to store sensitive information in CI/CD variables in gitlab-ci.yml because they are encrypted.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "Global variables are visible to the entire pipeline and job variables are only visible inside the job.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "You can only use pre-defined CI/CD variables in job rules.", "type": "s", "o": ["True", "False"], "a": ["False"]},
    {"q": "Rules in GitLab CI are equivalent to which of the following in Jenkins?", "type": "s", "o": ["always", "steps", "when"], "a": ["when"]},
    {"q": "A CI/CD component can be added to a gitlab-ci.yml pipeline using the include keyword.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "The GitLab system administrator can designate a project instance-wide collection of components.", "type": "s", "o": ["True", "False"], "a": ["True"]},
    {"q": "Which of the following are valid CI/CD component types in GitLab CI?", "type": "s", "o": ["stage component", "pipeline component", "variable component"], "a": ["pipeline component"]},
    {"q": "What are some business reasons for creating CI/CD pipelines? (Select all that apply)", "type": "m", "o": ["Deploys software earlier in the SDLC to find issues early", "Helps catch software bugs when they are less costly to fix", "Eliminate manual testing", "Devs don't have to run unit tests"], "a": ["Deploys software earlier in the SDLC to find issues early", "Helps catch software bugs when they are less costly to fix"]},
    {"q": "Which of the following best describes appropriate use cases for Jenkins and GitLab CI?", "type": "s", "o": ["Jenkins ideal for diverse requirements/large orgs; GitLab CI easier for smaller teams/SaaS", "GitLab requires manual config; Jenkins for simple projects", "Jenkins for smaller teams; GitLab for large enterprises"], "a": ["Jenkins ideal for diverse requirements/large orgs; GitLab CI easier for smaller teams/SaaS"]},
]

def run_quiz():
    random.shuffle(QUIZ_DATA)
    score = 0
    total = len(QUIZ_DATA)

    print("-" * 60)
    print("           DEVOPS & ENTERPRISE SYSTEMS: FULL QUIZ")
    print("-" * 60)
    print(f"Total Questions: {total}")
    print("Instructions:")
    print("1. For Single Choice/TF: Enter the letter (e.g., A)")
    print("2. For Select All: Enter letters separated by commas (e.g., A, C)")
    print("-" * 60 + "\n")

    for i, question in enumerate(QUIZ_DATA, 1):
        print(f"[{i}/{total}] {question['q']}")
        
        # Display options
        for idx, option in enumerate(question['o']):
            print(f"  {chr(65 + idx)}) {option}")
        
        user_input = input("\nYour Answer: ").upper().replace(" ", "").split(",")
        
        # Convert user letters back to text for comparison
        user_choices = []
        try:
            for letter in user_input:
                if letter:
                    idx = ord(letter) - 65
                    if 0 <= idx < len(question['o']):
                        user_choices.append(question['o'][idx])
        except:
            pass

        # Compare answers using sets
        if set(user_choices) == set(question['a']):
            print("\n✅ CORRECT!")
            score += 1
        else:
            print("\n❌ WRONG.")
            print(f"The correct answer(s) was: {', '.join(question['a'])}")
        
        print("=" * 40 + "\n")

    # Final Result
    percent = (score / total) * 100
    print("-" * 60)
    print(f"QUIZ COMPLETE")
    print(f"Total Score: {score} / {total} ({percent:.2f}%)")
    print("-" * 60)

if __name__ == "__main__":
    run_quiz()