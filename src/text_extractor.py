import subprocess

applescript = """
-- Helper function to create output directories
on createOutputDirectory(parentFolder)
	tell application "Finder"
		if not (exists folder (parentFolder & "output_text")) then
			make new folder at parentFolder with properties {name:"output_text"}
		end if
		if not (exists folder (parentFolder & "output_pdfs")) then
			make new folder at parentFolder with properties {name:"output_pdfs"}
		end if
		return {textFolder:(parentFolder & "output_text:"), pdfFolder:(parentFolder & "output_pdfs:")}
	end tell
end createOutputDirectory

-- Helper function to get base filename without extension
on getBaseName(fileName)
	set tid to AppleScript's text item delimiters
	set AppleScript's text item delimiters to "."
	set baseName to text items 1 thru -2 of fileName as string
	set AppleScript's text item delimiters to tid
	return baseName
end getBaseName

-- Main script
try
	-- 1. Set the folder directly (no need to prompt)
	set imageFolder to POSIX file "output_frames" as alias
	set outputFolders to my createOutputDirectory(imageFolder as text)
	set pdfFolder to pdfFolder of outputFolders -- Correctly reference the pdfFolder
	
	-- Get list of image files
	tell application "Finder"
		set imageFiles to files of folder imageFolder whose name extension is in {"jpg", "jpeg", "png", "tiff", "gif"}
	end tell
	
	-- 2. Process each file (PDF conversion)
	repeat with imageFile in imageFiles
		try
			set fileName to name of imageFile
			set baseName to my getBaseName(fileName)
			set pdfPath to (pdfFolder & baseName & ".pdf")
			
			-- Open the image file in Preview
			tell application "Preview"
				activate
				open imageFile
				delay 1 -- Give time to open
				
				-- Export the document as PDF with the correct AppleScript PDF type
				save front document in file pdfPath as «class PDF »
				close front document saving no
			end tell
			
		on error errMsg
			display dialog "Error processing file " & fileName & ": " & errMsg buttons {"OK"} default button "OK" with icon stop
		end try
	end repeat
	
	-- Success message
	display dialog "PDF conversion complete!" buttons {"OK"} default button "OK"
	
	-- New functionality: process PDFs in output_pdfs directory
	tell application "Finder"
		if not (exists folder pdfFolder) then
			error "The output_pdfs directory does not exist."
		end if
		
		-- Open output_pdfs folder
		open folder pdfFolder
		
		-- Get list of PDF files in the output_pdfs folder
		set pdfFiles to files of folder pdfFolder whose name extension is "pdf"
		
		repeat with pdfFile in pdfFiles
			try
				set pdfFileName to name of pdfFile
				set textFileName to my getBaseName(pdfFileName) & "_text.txt"
				set textPath to (textFolder of outputFolders & textFileName) as text
				
				-- Open the PDF in Preview
				tell application "Preview"
					activate
					open pdfFile
					delay 1
					
					-- Select all text
					tell application "System Events"
						tell process "Preview"
							keystroke "a" using command down
							delay 0.5
							
							-- Copy selected text
							keystroke "c" using command down
							delay 0.5
						end tell
					end tell
					
					-- Save the copied text to a file
					set textContent to the clipboard
					if textContent is not "" then
						try
							set textFile to open for access textPath with write permission
							set eof textFile to 0
							write textContent to textFile as text
							close access textFile
						on error errMsg
							close access textFile
							display dialog "Error saving text file: " & errMsg buttons {"OK"} default button "OK" with icon stop
						end try
					end if
					
					-- Close the PDF document
					close front document saving no
				end tell
				
			on error errMsg
				display dialog "Error processing PDF file " & pdfFileName & ": " & errMsg buttons {"OK"} default button "OK" with icon stop
			end try
		end repeat
	end tell
	
on error errMsg
	display dialog "Error: " & errMsg buttons {"OK"} default button "OK"
end try
"""

def text_extractor():
    subprocess.run(["osascript", "-e", applescript], check=True)
