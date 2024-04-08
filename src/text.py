""" Module that contains predefined text blocks to display in GUI """

SIDEBAR_CONTENT = """
            # Unofficial KIT Grade Analyzer

            - Simply put the URL to the PDF in the corresponding field and click on the button.
            - You can find the ECTS Ranking Chart here: 
            `https://www.sle.kit.edu/nachstudium/ects-einstufungstabellen.php`
            - Only works with the german version and with the newer version of the documents (i.e. the ones
            with the cumulative column)
            - Example URL would be 
            `https://www.sle.kit.edu/dokumente/ects-tabellen//ECTS_Tab_WS23_24_MA_Informatik_DE.pdf`  
            - To compare two or more cohorts, simply add them into the text field separated by '$'

            ___
            *Made by Alessio Negrini*  
            *Contact: Alessio(d0t|]Negrini[at)live.de*
            *Version 0.1, March 2024*
        """


INTRO_CONTENT = """
            ## 👋 Hi and welcome to the Unofficial KIT Grade Analyzer  
            **How To Use**  
            - Please enter one or more URL to the PDF document that you'd like to analyze
            - If you are using multiple URLs, please separate them using Seperator Token '\$', e.g. `<URL1>$<URL2>`
            - You can find the ECTS Ranking Chart here: `https://www.sle.kit.edu/nachstudium/ects-einstufungstabellen.php`  
                - Simply click on your cohort and copy the URL to your pdf
                - Note that this Data App only works with never versions of the Ranking (i.e. the ones with the cumulative column)
            """
