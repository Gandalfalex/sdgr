import { BASE_URL } from "../api/ApiConnector";

export const DocumentationPage = () => {
  return (
    <div>
      <h1>Documentation</h1>
      <ul>
        <li>
          <a href={`${BASE_URL}/docs`} target="_blank" rel="noreferrer">
            Website 1 - Docs
          </a>
        </li>
        <li>
          <a
            href={`${BASE_URL}/springboot/swagger-ui/index.html`}
            target="_blank"
            rel="noreferrer"
          >
            Website 2 - SpringBoot Swagger
          </a>
        </li>
        <li>
          <a
            href={`${BASE_URL}/django/swagger`}
            target="_blank"
            rel="noreferrer"
          >
            Website 3 - Django Swagger
          </a>
        </li>
      </ul>
    </div>
  );
};
