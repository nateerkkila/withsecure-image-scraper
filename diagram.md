```mermaid
graph TD
    subgraph "Development & SCM"
        A[<fa:fa-user> Developer] -->|1. git push & create PR| B[<fa:fa-code-branch> GitHub Repository];
    end

    subgraph "GitHub Actions Platform (Orchestration)"
        B --> C{PR Validation Workflow};
        B -->|3. Merge to main| E{CI/CD Workflow};
        C --> D;
        E --> D;
    end

    subgraph "AWS Cloud: CI Execution"
        subgraph D ["<fa:fa-server> Self-Hosted EC2 Runner"]
            direction LR
            S1["**Stage 1: Linting**\n- black\n- flake8"];
            S2["**Stage 2: Testing**\n- pytest\n- pytest-cov"];
            S3["**Stage 3: Build Image**\n- docker build"];
            S1 --> S2 --> S3;
        end
    end

    subgraph "Artifact & Secret Management"
        F[<fa:fa-box-archive> GitHub Container Registry]
        G[<fa:fa-key> GitHub Encrypted Secrets]
        S3 -->|4. docker push| F;
        D -->|Get Secrets| G;
    end

    subgraph "AWS Cloud: Production Environment"
        H[**Target EC2 Instance**];
        subgraph H
            direction LR
            H1[Docker Engine] --> H2[<fa:fa-play> Running Container];
        end
    end
    
    D -->|5. Deploy via SSH| H;
    H1 -->|6. docker pull| F;
    
    subgraph "Monitoring & Feedback Loop"
        I["<fa:fa-chart-line> Monitoring & Alerting\n(e.g. CloudWatch)"];
        J["<fa:fa-slack> Slack Notification"];
        H2 --> I;
        E -->|7. Send Status| J;
        J -->|8. Feedback| A;
        I -->|Feedback| A;
    end

    style A fill:#cde4ff
    style B fill:#cde4ff
    style F fill:#e6ffcc
    style G fill:#e6ffcc
    style H fill:#d4edda
    style I fill:#fff0b3
    style J fill:#fff0b3
    ```