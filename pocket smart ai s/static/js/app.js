async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "include",
            ...options
        }
    );


    let data = {};

    try {

        data = await response.json();

    } catch {

        data = {};

    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );
    }


    return data;
}


function formObject(form) {

    return Object.fromEntries(
        new FormData(form).entries()
    );
}


function money(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(
        Number(value || 0)
    );
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function (character) {

            return {

                "&": "&amp;",

                "<": "&lt;",

                ">": "&gt;",

                '"': "&quot;",

                "'": "&#039;"

            }[character];
        }
    );
}


function escapeAttr(value) {

    return escapeHtml(value)
        .replace(
            /`/g,
            "&#096;"
        );
}


function renderResult(data) {

    const result =
        document.getElementById(
            "result"
        );


    if (!result) {
        return;
    }


    result.innerHTML = `

        <div class="card">

            <span class="source">

                ${escapeHtml(
                    data.source || "AI"
                )}

            </span>


            <h2>

                ${escapeHtml(
                    data.summary ||
                    "Recommendations"
                )}

            </h2>


            <div class="allocation">

                ${
                    Object.entries(
                        data.allocation || {}
                    )
                    .map(
                        ([key, value]) => `

                        <div class="alloc">

                            <span>
                                ${escapeHtml(key)}
                            </span>

                            <b>
                                ${money(value)}
                            </b>

                        </div>

                    `
                    )
                    .join("")
                }

            </div>


            <h3>
                Recommendations
            </h3>


            ${
                (data.recommendations || [])
                .map(
                    recommendation => `

                    <div class="rec">

                        <div class="rec-head">

                            <b>
                                ${escapeHtml(
                                    recommendation.name
                                )}
                            </b>

                            <span class="price">

                                ${money(
                                    recommendation.estimated_price
                                )}

                            </span>

                        </div>


                        <p class="small">

                            ${escapeHtml(
                                recommendation.description
                            )}

                        </p>


                        <a
                            class="small"
                            target="_blank"
                            rel="noopener"
                            href="${escapeAttr(
                                recommendation.search_url
                            )}"
                        >

                            Search on
                            ${escapeHtml(
                                recommendation.platform
                            )}

                        </a>

                    </div>

                `
                )
                .join("")
            }


            <h3>
                Tips
            </h3>


            <ul>

                ${
                    (data.tips || [])
                    .map(
                        tip => `
                            <li>
                                ${escapeHtml(tip)}
                            </li>
                        `
                    )
                    .join("")
                }

            </ul>

        </div>

    `;
}


function requireLogin(error) {

    if (
        String(
            error.message
        )
        .toLowerCase()
        .includes(
            "authentication"
        )
    ) {

        location.href = "/login";

    } else {

        alert(
            error.message
        );
    }
}


function bindLogin() {

    const form =
        document.getElementById(
            "loginForm"
        );


    if (!form) {
        return;
    }


    form.onsubmit =
        async function (event) {

            event.preventDefault();


            const message =
                document.getElementById(
                    "message"
                );


            try {

                const data =
                    formObject(form);


                await api(
                    "/login",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)

                    }
                );


                message.textContent =
                    "Login successful";

                message.className =
                    "message success";


                location.href =
                    "/dashboard";


            } catch (error) {

                message.textContent =
                    error.message;
            }
        };
}


function bindRegister() {

    const form =
        document.getElementById(
            "registerForm"
        );


    if (!form) {
        return;
    }


    form.onsubmit =
        async function (event) {

            event.preventDefault();


            const message =
                document.getElementById(
                    "message"
                );


            try {

                const data =
                    formObject(form);


                await api(
                    "/register",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)

                    }
                );


                message.textContent =
                    "Registration successful. Redirecting...";

                message.className =
                    "message success";


                setTimeout(
                    function () {

                        location.href =
                            "/login";

                    },
                    700
                );


            } catch (error) {

                message.textContent =
                    error.message;
            }
        };
}


function bindHomePlanner() {

    const form =
        document.getElementById(
            "homeForm"
        );


    if (!form) {
        return;
    }


    form.onsubmit =
        async function (event) {

            event.preventDefault();


            try {

                const data =
                    formObject(form);


                data.budget =
                    Number(
                        data.budget
                    );


                data.items =
                    (
                        data.items || ""
                    )
                    .split(",")
                    .map(
                        item =>
                            item.trim()
                    )
                    .filter(
                        Boolean
                    );


                const result =
                    await api(
                        "/generate-home",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(data)

                        }
                    );


                renderResult(result);


            } catch (error) {

                requireLogin(error);

            }
        };
}


function bindPartyPlanner() {

    const form =
        document.getElementById(
            "partyForm"
        );


    if (!form) {
        return;
    }


    form.onsubmit =
        async function (event) {

            event.preventDefault();


            try {

                const data =
                    formObject(form);


                data.budget =
                    Number(
                        data.budget
                    );


                data.guests =
                    Number(
                        data.guests
                    );


                const result =
                    await api(
                        "/generate-party",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(data)

                        }
                    );


                renderResult(result);


            } catch (error) {

                requireLogin(error);

            }
        };
}


function bindJewelryPlanner() {

    const form =
        document.getElementById(
            "jewelryForm"
        );


    if (!form) {
        return;
    }


    form.onsubmit =
        async function (event) {

            event.preventDefault();


            try {

                const formData =
                    new FormData(form);


                formData.set(
                    "budget",
                    Number(
                        formData.get(
                            "budget"
                        )
                    )
                );


                const result =
                    await api(
                        "/generate-jewelry",
                        {

                            method: "POST",

                            body:
                                formData

                        }
                    );


                renderResult(result);


            } catch (error) {

                requireLogin(error);

            }
        };
}


async function loadDashboard() {

    try {

        const data =
            await api(
                "/session-info"
            );


        const welcome =
            document.getElementById(
                "welcome"
            );


        const account =
            document.getElementById(
                "account"
            );


        if (welcome) {

            welcome.textContent =
                `Welcome, ${data.name}.`;
        }


        if (account) {

            account.textContent =
                `${data.name} · ${data.email}`;
        }


    } catch {

        location.href =
            "/login";
    }
}


async function logout() {

    await api(
        "/logout",
        {
            method: "POST"
        }
    );


    location.href =
        "/login";
}


async function loadHistory() {

    const container =
        document.getElementById(
            "history"
        );


    if (!container) {
        return;
    }


    try {

        const rows =
            await api(
                "/history"
            );


        if (!rows.length) {

            container.innerHTML = `

                <div class="empty">

                    No recommendation
                    history yet.

                </div>

            `;

            return;
        }


        container.innerHTML =
            rows
            .map(
                row => `

                <details>

                    <summary>

                        <b>
                            ${escapeHtml(
                                row.planner_type
                            )}
                        </b>

                        ·

                        ${money(
                            row.budget
                        )}

                        ·

                        ${new Date(
                            row.created_at
                        ).toLocaleString()}

                    </summary>


                    <div
                        style="padding-top:12px"
                    >

                        ${escapeHtml(
                            row.result.summary ||
                            "Saved recommendation"
                        )}

                    </div>

                </details>

            `
            )
            .join("");


    } catch (error) {

        container.innerHTML = `

            <div class="empty">

                ${escapeHtml(
                    error.message
                )}

                <br>

                <a href="/login">
                    Login
                </a>

            </div>

        `;
    }
}