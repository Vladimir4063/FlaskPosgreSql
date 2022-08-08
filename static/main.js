// me ubido con el id del form
const userForm = document.querySelector('#userForm')


let users = []
editing = false
userId = null
// DOMContentLoaded es lo primero que se ejecuta cuando carga la pag
window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/users')
    const data = await response.json()
    users = data
    renderUser(users)
})


// escucho si sucede algun evento o click
userForm.addEventListener('submit', async e => {
    e.preventDefault()

    // console.log(e) //veo el evento

    // obtengo el valor
    const username = userForm["username"].value
    const email = userForm["email"].value
    const password = userForm["password"].value

    console.log(username, email, password);

    if (!editing) {
      const response = await fetch("/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password,
        }),
      });

      const data = await response.json(); // guardo la respuesta del POST y la muestro por consola
      // console.log(data)

      users.unshift(data); // añado al principio de la lista

    }else{
        const response = await fetch("/api/users",{
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            }),
        })
        const data = await response.json();
        console.log(data)
    }
    // funcion que envia al back-end
    
    
    renderUser(users)

    // reseteo el formulario
    userForm.reset()
})

function renderUser(){
    const userList = document.querySelector('#userList')
    userList.innerHTML = ''

    users.forEach(user => {
      const userItem = document.createElement("li");
      userItem.classList = "list-group-item list-group-item-dark my-2"; //estilos del card
      // agrego con un for en el html
      userItem.innerHTML = `
        <header class="d-flex justify-content-between align">
            <h3>${user.username}</h3>
            <div>
                <button class="btn-edit btn btn-secondary btn-sm">edit</button>
                <button class="btn-delete btn btn-danger btn-sm">delete</button>
            </div>
        </header>
            <p>${user.email}</p>
            <p class="text-truncate">${user.password}</p>
        `

      // Encuentro el id para eliminar
      const btnDelete = userItem.querySelector(".btn-delete");

      btnDelete.addEventListener("click", async () => {
        const response = await fetch(`/api/users/${user.id}`, {
          method: "DELETE",
        });

        // convierto la respuesta y veo en consola
        const data = await response.json();
        
        // filtro la nueva list
        users = users.filter(user => user.id !== data.id)
        renderUser(users)
        });
        userList.append(userItem);

        
        // Editar
      const btnEdit = userItem.querySelector(".btn-edit")

      btnEdit.addEventListener("click", async (e) => {
          const response = await fetch(`/api/users/${user.id}`)
          const data = await response.json()
        
          userForm["username"].value = data[1];
          userForm["email"].value = data[3];

          editing = true
          userId = data.id
          console.log(userId)

      })
    })
}
