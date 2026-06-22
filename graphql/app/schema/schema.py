type User {
    id : ID!
    name : String!
    email : String!
    tasks : [Tasks!]!
    project : [Projects!]!         

}


type Project {
    id :ID!
    name : String!
    owner : [User!]!
    tasks : [Tasks!]!         
}


type Status {
    id : ID !
    name : String!
    tasks : [Tasks!]!
}


type Tasks {
    id : ID!
    title : String!
    project : Project!
    assignee : User!
    status : Status! 
}