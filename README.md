# ChatGPTServer by Curtis White 
This is a ChatGPT to API and ChatGPT Augmentation System. This enables a few things primarily:

1. You can use your ChatGPT as a local API. This is for ChatGPT power users and not for automated / bot activity. 
2. Enabled ChatGPT to run client side code.
3. Augment CHatGPT capabilities with a dynamic growing set of abilities known as the Mecha Corp system.
4. My greater goal is really even even more about extending human capability.
   
*** 
Warning: There is no code containment nor safety. Be extremely careful. 
Run at own risk! Do not use for production. You are responsible for any and all damages. 
Risk of running unsandbox client side code are numerous but for example if you were using a browser extension, it might be possible for someone to poison a URL 
and evoke code on your maachine. 

Caution: The Javascript code monitors your chat to send to your local running host. 

Cuation: System is still extremely tricky and bug prone. 
***

### Why Client Side Code?
 
 1. Extend its's capabilities by adding persistent capabilities
 2. Accesss to any and all Python modules / functions
 3. Create more efficient work flows. Example, it can create the entire file system for a project vs. copy/paste. 
 4. Ability to parse local data / large data without having to zip it.
 5. Capture workflow better and other many other benefits.
 6. It can act more as a conscious etension / OS extension. Some really transformative potential.

### Mecha Corp Capabilities:
1. Augmented engine structure for creating and getting augmented capabilities in a standardized way vs temporary work functions.
2. Task manage / to-do lists for state tracking
3. Logging capability for large file processing and "memory tracking"
4. Preview file capabilities 
5. Prompt / Instruction Chains

### To Do Add More Capabiltiies
1. Add web scraping capability for general research assistant.
2. Add document store / stacks for research.
3. Create capability to ask an "out of context" AI queries for multi-modal like ChatGPT, Bard, llama code,
# etc for error correction
# 4. Add new capabilities like voice
# 5. Add streaming and recording for automatic creation local markdowns
# 6. Add project creation automation for files system creation

### System Architecture

1. System consist of Tamper Monkey JS. Must install the JS into TamperMonkey.
2. A Flask Python server
3. Python work file that acts as a dynamic persistent augmented capabilities extension. Work is also piped into this which can be periodically changed out
via template.
4. Work is piped to a ipynb for the user but not executed.

### Quickstart

1. Install the TamperMonkey script.
2. Start Python Flask Server
3. ChatGPT will be able to run code on client side by emitting a codeblock with # pyclient comment. It must be a code block. Multiple code blocks can be processed.
4. Work.py file has the Mecha Corp extensions and also acts as a work file where Python can be piped.

### Known Issues / Help
1. The button regenerate/continue button must be visible for the injection to work.
2. The server restart / reload code likely is not working properly. 
3. You will likely need to keep work.py open in Visual Studio to triage.
4. It is intended to be used with Code Interpreter model. Prompting to get it to understand the new capabilities is not always easy. Prompts will be coming soon.

### Background

Originally the intention was to use Jupyter notebook for the augmentated capabilities. It was always tantalizing close to working.
But, I ran into too many problems with slow execution or other problems so the augmentated capabilities was shifted to Python dynamic file. See the
work and template.

Special thanks & See Also Similar Project:
https://github.com/zsodur/chatgpt-api-by-browser-script 





   
