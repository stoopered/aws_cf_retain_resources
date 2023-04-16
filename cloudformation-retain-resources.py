 import boto3
 import os
 import json
 
 cf_client = boto3.client('cloudformation')
 
 stack_prefix = input("Enter stack name prefix: ")
 delete_stacks = input("Delete Stacks? (y/n): ")
 
 #solutions-dev-lambda-pdfgenerator
 
 # Initialize the NextToken variable required to retrieve stacks
 next_token = None
 
 # Initialize lists for updated and deleted stacks
 updated_stacks = []
 deleted_stacks = []
 
 # Keep looping until all matching stacks have been processed
 while True:
     # Call describe_stacks() to get the next page of stack information
     if next_token:
         stack_data = cf_client.describe_stacks(NextToken=next_token)
     else:
         stack_data = cf_client.describe_stacks()
 
     # Filter the stacks based on the prefix (if specified)
     if stack_prefix:
         stacks = [s for s in stack_data['Stacks'] if s['StackName'].startswith(stack_prefix)]
     else:
         stacks = stack_data['Stacks']
 
     # Process each matching stack
     for stack in stacks:
         stack_name = stack['StackName']
         # Construct a filename based on the stack name and prefix (if any)
         filename = f"{stack_name}.json"
         # Get the stack template summary as a dictionary
         response = cf_client.get_template(StackName=stack_name)
         template_body = response['TemplateBody']
 
         # Add "DeletionPolicy": "Retain" to each resource in the CloudFormation template
         for resource_name, resource in template_body['Resources'].items():
             resource['DeletionPolicy'] = 'Retain'
 
         # Save the updated template to a file
         with open(filename, 'w') as f:
             json.dump(template_body, f, indent=4)
             print(f"Downloaded {stack_name} stack.")
             print(f"Saved file as {os.path.abspath(filename)}")
 
         # Update the stack with the updated template and parameters
         with open(filename, 'r') as f:
             updated_template_body = f.read()
             
         parameter_values = []
         
         for parameter in stack['Parameters']:
             parameter_values.append({
                 'ParameterKey': parameter['ParameterKey'],
                 'UsePreviousValue': True
             })
         try:    
             print(f"Updating stack: {stack}")
             cf_client.update_stack(
                 StackName=stack_name,
                 TemplateBody=updated_template_body,
                 Parameters=parameter_values
             )
         except:
             print(f"{stack_name} has no updates")
             pass
         
         updated_stacks.append(stack_name)
         print(f"Updated {stack_name} stack with the updated template.")
 
     # Check if there are more pages of stack information
     if 'NextToken' in stack_data:
         next_token = stack_data['NextToken']
     else:
         break
 
     # Delete stacks that were not updated
     if delete_stacks.lower() == 'y':
         for stack in stacks:
             print(f"Deleting stack: {stack}")
             if stack['StackName'] in updated_stacks:
                 cf_client.delete_stack(StackName=stack['StackName'])
                 deleted_stacks.append(stack['StackName'])
                 print(f"Deleted {stack['StackName']} stack.")
 
 # Output a list of updated and deleted stacks to a text file
 with open('updated_stacks.txt', 'w') as f:
     f.write('\n'.join(updated_stacks))
     print(f"List of updated stacks saved as {os.path.abspath('updated_stacks.txt')}.")
 with open('deleted_stacks.txt', 'w') as f:
     f.write('\n'.join(deleted_stacks))
     print(f"List of deleted stacks saved as {os.path.abspath('deleted_stacks.txt')}.")
