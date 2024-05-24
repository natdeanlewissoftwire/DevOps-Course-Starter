workspace {

    model {
        user = person "User"
        wicrosoftToDo = softwareSystem "Wicrosoft To-Do" "Allows the user to view, add, edit and remove to-do tasks" {
            tags "NewSystem"
            flask = container "Flask" {
                tags "NewSystem"
            }
            applicationCode = container "Application code" {
                tags "NewSystem"
                app = component "app.py" "Handles routing to the different pages of the web app" {
                    tags "NewSystem"
                }
                trello_items = component "trello_items.py" "Requests the Trello API to add, edit and remove tasks" {
                    tags "NewSystem"
                }
                view_model = component "view_model.py" "Groups tasks by status for passing to views" {
                   tags "NewSystem"
                }
            }
        }

        trello = softwareSystem "Trello" "The source of truth for the user's tasks"


        user -> wicrosoftToDo "Uses"
        wicrosoftToDo -> trello "Reads from and writes to"
        flask -> applicationCode "Runs"
        app -> trello_items "Uses"
        app -> view_model "Uses"

    }

    views {
        systemContext wicrosoftToDo "systemContext" {
            include *
        }

        container wicrosoftToDo "container" {
            include *
            autoLayout lr
        }

        component applicationCode "component" {
            include *
            autoLayout lr
        }


        styles {
            element "NewSystem" {
                background #1168bd
                color #ffffff
            }

            element "Person" {
                shape Person
                background #1168bd
                color #ffffff
            }
        }
    }
}