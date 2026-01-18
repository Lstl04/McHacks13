## Inspiration
AIly was born from watching our parents run their own small businesses. We saw firsthand the "second shift" they worked after work, spending hours at the kitchen table sorting through stacks of paper receipts and trying to fix a messy handwritten schedule after a long day of physical work.

Small businesses are the backbone of our communities, but the people running them are often forced to use tools that are either too complicated or completely outdated. Our goal is to give that time back to them. By streamlining the most frustrating parts of the job, we want to make life easier for the people who keep our society running. We believe they deserve technology that works as hard as they do.

## What it does
AIly is a central command center that manages jobs, expenses, clients, and invoices to provide a real-time view of business health and profitability. An integrated chatbot with access to the full operational history allows owners to query past performance for instant insights, while speech-to-text integration automates high-friction tasks like voice-generating invoices or adding calendar events. This streamlines the entire administrative workflow, turning manual paperwork into an automated, voice-driven process.

## How we built it
We built the platform with a focus on speed and security. For the core, we chose React for the frontend and FastAPI on the backend to keep things responsive and efficient. To handle user accounts and keep everything secure, we integrated Auth0, while MongoDB serves as our primary database for storing all the business records and operational history.

For the intelligence side, we used Gumloop to orchestrate our AI workflows and manage the chatbot's logic. To make the app truly hands-free, we brought in ElevenLabs for the speech-to-text integration, which is what allows owners to handle their admin tasks just by speaking while they work.

## Challenges we ran into
We kept the project modular even though we were learning most of these tools as we went. It was a constant balancing act: trying to integrate Auth0, Gumloop, and ElevenLabs without letting the backend turn into "spaghetti" code where everything was too tangled to fix easily.

Working together was also a lot harder than we expected. Since we were working on separate branches, we ran into multiple messy merge conflicts. We had the same issues during deployment, where things that worked fine on our laptops broke on the server.

The hardest part was just deciding what not to build. When you're on a tight deadline, you have to be decide about cutting out the "fun" features that are actually overkill for the hackathon, focusing instead on making sure the core stuff didn't break.

## Accomplishments that we're proud of
We’re especially proud of the AI chatbot we built. It’s not just for conversation; it can actually launch Gumloop workflows, answer general questions, and pull specific business data from the database to provide real insights. We worked hard to make the overall infrastructure as user-friendly as possible so it feels natural to use. We also pushed ourselves to integrate MongoDB and Auth0, two technologies we hadn’t worked with before, and we’re proud that we were able to get them fully functional and secure within the app.

## What we learned
Building this project taught us that speed isn't just about output; it's about how quickly you can adapt to new tools. Integrating Auth0, Gumloop, and ElevenLabs in a single weekend meant we had to learn their APIs on the fly and bridge different systems together without compromising the core infrastructure.

A major takeaway was learning when to decide if a feature was "overkill." It's easy to get distracted by complex ideas, but we had to keep the focus on the end-user: business owners who need tools that are rugged and reliable. We learned to prioritize no-nonsense logic over technical vanity, ensuring the app remained functional and accessible.

The strict time constraint forced us to be disciplined with our "feature triage." We had to make hard calls on what to build based on what would provide the most immediate value. Ultimately, it was a lesson in high-trust collaboration. By leaning on each other’s specific strengths, we were able to move as a single unit and turn the concept into a working product.

## What's next for AIly
Moving forward, we plan to speak directly with small business owners to better understand their daily needs without the pressure of a deadline. This feedback will be essential for refining the user experience and ensuring the tool solves real-world operational problems.

Technically, our next steps include adding robust sanity checks to our AI workflows and expanding our library of third-party integrations. We also aim to build a client-facing portal that allows customers to interact directly with the business calendar to book appointments, further automating the scheduling process and reducing manual back-and-forth.
