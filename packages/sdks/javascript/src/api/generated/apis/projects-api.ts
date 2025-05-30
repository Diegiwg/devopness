/* eslint-disable */
/**
 * devopness API
 * Devopness API - Painless essential DevOps to everyone 
 *
 * The version of the OpenAPI document: latest
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { ApiBaseService } from "../../../services/ApiBaseService";
import { ApiResponse } from "../../../common/ApiResponse";
import { ArgumentNullException } from "../../../common/Exceptions";
import { ApiError } from '../../generated/models';
import { Project } from '../../generated/models';
import { ProjectCreate } from '../../generated/models';
import { ProjectRelation } from '../../generated/models';
import { ProjectUpdate } from '../../generated/models';

/**
 * ProjectsApiService - Auto-generated
 */
export class ProjectsApiService extends ApiBaseService {
    /**
     * 
     * @summary Create a project for a user or an organization
     * @param {ProjectCreate} projectCreate A JSON object containing the resource data
     */
    public async addProject(projectCreate: ProjectCreate): Promise<ApiResponse<Project>> {
        if (projectCreate === null || projectCreate === undefined) {
            throw new ArgumentNullException('projectCreate', 'addProject');
        }

        let queryString = '';

        const requestUrl = '/projects' + (queryString? `?${queryString}` : '');

        const response = await this.post <Project, ProjectCreate>(requestUrl, projectCreate);
        return new ApiResponse(response);
    }

    /**
     * 
     * @summary Get a Project by ID
     * @param {number} projectId The ID of the project.
     */
    public async getProject(projectId: number): Promise<ApiResponse<Project>> {
        if (projectId === null || projectId === undefined) {
            throw new ArgumentNullException('projectId', 'getProject');
        }

        let queryString = '';

        const requestUrl = '/projects/{project_id}' + (queryString? `?${queryString}` : '');

        const response = await this.get <Project>(requestUrl.replace(`{${"project_id"}}`, encodeURIComponent(String(projectId))));
        return new ApiResponse(response);
    }

    /**
     * 
     * @summary Return a list of all projects the current user has access to
     * @param {number} [page] Number of the page to be retrieved
     * @param {number} [perPage] Number of items returned per page
     */
    public async listProjects(page?: number, perPage?: number): Promise<ApiResponse<Array<ProjectRelation>>> {

        let queryString = '';
        const queryParams = { page: page, per_page: perPage, } as { [key: string]: any };
        for (const key in queryParams) {
            if (queryParams[key] === undefined || queryParams[key] === null) {
                continue;
            }

            queryString += (queryString? '&' : '') + `${key}=${encodeURI(queryParams[key])}`;
        }

        const requestUrl = '/projects' + (queryString? `?${queryString}` : '');

        const response = await this.get <Array<ProjectRelation>>(requestUrl);
        return new ApiResponse(response);
    }

    /**
     * 
     * @summary Update an existing Project
     * @param {number} projectId The ID of the project.
     * @param {ProjectUpdate} projectUpdate A JSON object containing the resource data
     */
    public async updateProject(projectId: number, projectUpdate: ProjectUpdate): Promise<ApiResponse<void>> {
        if (projectId === null || projectId === undefined) {
            throw new ArgumentNullException('projectId', 'updateProject');
        }
        if (projectUpdate === null || projectUpdate === undefined) {
            throw new ArgumentNullException('projectUpdate', 'updateProject');
        }

        let queryString = '';

        const requestUrl = '/projects/{project_id}' + (queryString? `?${queryString}` : '');

        const response = await this.put <void, ProjectUpdate>(requestUrl.replace(`{${"project_id"}}`, encodeURIComponent(String(projectId))), projectUpdate);
        return new ApiResponse(response);
    }
}
