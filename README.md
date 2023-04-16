# CloudFormation Stack Updater and Deleter
This Python script uses the Boto3 library to interact with the AWS CloudFormation service. It can search for CloudFormation stacks in your AWS account, update the stack templates by adding "DeletionPolicy": "Retain" to each resource, and delete the stacks based on user input.

# Updating CloudFormation Templates
The script first prompts the user to enter a stack name prefix, which can be used to search for specific stacks or all stacks in the account. It then uses the CloudFormation describe_stacks() API to retrieve information about the stacks matching the prefix. For each stack, it retrieves the stack template using the get_template() API and adds "DeletionPolicy": "Retain" to each resource in the template.

The updated template is then saved to a JSON file with the same name as the stack. Finally, the script updates the stack with the new template using the update_stack() API.

# Deleting CloudFormation Stacks
After updating the templates, the script prompts the user whether to delete any stacks. If the user chooses to delete, the script loops through the stacks and deletes them using the delete_stack() API. The names of the updated and deleted stacks are saved to a text file called updated_and_deleted_stacks.txt.

Note that deleting a stack cannot be undone and may result in the loss of resources provisioned by the stack. Therefore, use caution when using the deletion feature of this script.

# AWS CloudFormation Stack Updater

This Python script updates all AWS CloudFormation stacks with a specified prefix to add a `DeletionPolicy: Retain` property to each resource in the stack's template. It can also delete stacks based on user input.

## Requirements

- Python 3.x
- boto3 library
- AWS CLI configured with valid credentials

## Usage

1. Clone the repository and navigate to the root directory.
2. Install the boto3 library by running `pip install boto3`.
3. Run the script with `python stack_updater.py`.
4. Follow the prompts to update or delete stacks.

## Contributing

Contributions are welcome! Please open an issue or pull request for any bug fixes or feature requests.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
