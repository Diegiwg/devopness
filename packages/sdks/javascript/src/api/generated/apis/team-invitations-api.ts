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

/**
 * TeamInvitationsApiService - Auto-generated
 */
export class TeamInvitationsApiService extends ApiBaseService {
    /**
     * 
     * @summary Accept a pending team invitation
     * @param {string} teamInvitationId The ID of the team invitation.
     */
    public async acceptTeamInvitation(teamInvitationId: string): Promise<ApiResponse<void>> {
        if (teamInvitationId === null || teamInvitationId === undefined) {
            throw new ArgumentNullException('teamInvitationId', 'acceptTeamInvitation');
        }

        let queryString = '';

        const requestUrl = '/team-invitations/{team_invitation_id}/accept' + (queryString? `?${queryString}` : '');

        const response = await this.post <void>(requestUrl.replace(`{${"team_invitation_id"}}`, encodeURIComponent(String(teamInvitationId))));
        return new ApiResponse(response);
    }

    /**
     * 
     * @summary Delete a pending team invitation
     * @param {string} teamInvitationId The ID of the team invitation.
     */
    public async deleteTeamInvitation(teamInvitationId: string): Promise<ApiResponse<void>> {
        if (teamInvitationId === null || teamInvitationId === undefined) {
            throw new ArgumentNullException('teamInvitationId', 'deleteTeamInvitation');
        }

        let queryString = '';

        const requestUrl = '/team-invitations/{team_invitation_id}' + (queryString? `?${queryString}` : '');

        const response = await this.delete <void>(requestUrl.replace(`{${"team_invitation_id"}}`, encodeURIComponent(String(teamInvitationId))));
        return new ApiResponse(response);
    }

    /**
     * 
     * @summary Reject a pending team invitation
     * @param {string} teamInvitationId The ID of the team invitation.
     */
    public async rejectTeamInvitation(teamInvitationId: string): Promise<ApiResponse<void>> {
        if (teamInvitationId === null || teamInvitationId === undefined) {
            throw new ArgumentNullException('teamInvitationId', 'rejectTeamInvitation');
        }

        let queryString = '';

        const requestUrl = '/team-invitations/{team_invitation_id}/reject' + (queryString? `?${queryString}` : '');

        const response = await this.post <void>(requestUrl.replace(`{${"team_invitation_id"}}`, encodeURIComponent(String(teamInvitationId))));
        return new ApiResponse(response);
    }
}
