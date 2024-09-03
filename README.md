# Towel Code Combiner

### 🖥️ Packaging on Mac with Custom Icon for `list_all_files.py`:

1. **Install PyInstaller**:
   - Open Terminal and run:
     ```bash
     pip install pyinstaller
     ```

2. **Create a Spec File (Optional)**:
   - Customize the packaging by generating a `.spec` file:
     ```bash
     pyinstaller --name "TowelCodeCombiner" --onefile --windowed /Users/towelwet/Downloads/list_all_files.py
     ```

3. **Add Custom Icon**:
   - Use the following command to include your custom icon:
     ```bash
     pyinstaller --name "TowelCodeCombiner" --onefile --windowed --icon="/Users/towelwet/Pictures/(Towel Apps)/Towel Code Combiner/tcc.jpg" /Users/towelwet/Downloads/list_all_files.py
     ```

4. **Build the Application**:
   - Run PyInstaller with the customized command:
     ```bash
     pyinstaller --onefile --windowed --icon="/Users/towelwet/Pictures/(Towel Apps)/Towel Code Combiner/tcc.jpg" /Users/towelwet/Downloads/list_all_files.py
     ```
   - This will create a standalone `.app` file in the `dist` folder.

5. **Test the Application**:
   - Navigate to the `dist` folder and run the `.app` file to ensure it works.

6. **Distribute**:
   - Zip the `.app` file and distribute it to your users.

---

### 🖥️ Step-by-Step Guide for Packaging on Windows

1. **Install PyInstaller**:
   - Open Command Prompt and run the following command to install PyInstaller:
     ```bash
     pip install pyinstaller
     ```

2. **Create a Spec File (Optional but Recommended)**:
   - Generate a `.spec` file if you want to customize the build process (e.g., adding data files, custom hooks, etc.). This step is optional but useful for more complex packaging requirements:
     ```bash
     pyinstaller --name "TowelCodeCombiner" --onefile --noconsole "C:\Users\Iv\Downloads\TCC All Files\list_all_files.py"
     ```

3. **Add Custom Icon**:
   - To include your custom icon, use the `--icon` option. Run the following command:
     ```bash
     pyinstaller --name "TowelCodeCombiner" --onefile --noconsole --icon="C:\Users\Iv\Downloads\TCC All Files\Towel Code Combiner\tcc.jpg" "C:\Users\Iv\Downloads\TCC All Files\list_all_files.py"
     ```

4. **Build the Application**:
   - After running the above command, PyInstaller will create a standalone `.exe` file in the `dist` folder. The full command is as follows:
     ```bash
     pyinstaller --onefile --noconsole --icon="C:\Users\Iv\Downloads\TCC All Files\Towel Code Combiner\tcc.jpg" "C:\Users\Iv\Downloads\TCC All Files\list_all_files.py"
     ```

5. **Test the Application**:
   - Navigate to the `dist` folder where the `.exe` file is located:
     ```bash
     cd dist
     ```
   - Run the `.exe` file to ensure it works as expected.

6. **Create an Installer (Optional)**:
   - If you want to create an installer package for easier distribution, you can use Inno Setup or a similar tool.
   - Follow the instructions in Inno Setup to include your `.exe` file and any additional resources.

7. **Distribute**:
   - Once the installer is created, you can distribute it as needed.
