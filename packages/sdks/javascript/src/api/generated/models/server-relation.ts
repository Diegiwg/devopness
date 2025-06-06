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


import { ActionRelationShallow } from './action-relation-shallow';
import { ActionStatus } from './action-status';
import { CredentialRelation } from './credential-relation';

/**
 * 
 * @export
 * @interface ServerRelation
 */
export interface ServerRelation {
    /**
     * The unique id of the given record
     * @type {number}
     * @memberof ServerRelation
     */
    id: number;
    /**
     * The id of the user who created the server and to whom the server belongs
     * @type {number}
     * @memberof ServerRelation
     */
    created_by: number;
    /**
     * The server\'s name
     * @type {string}
     * @memberof ServerRelation
     */
    name: string;
    /**
     * The server\'s hostname
     * @type {string}
     * @memberof ServerRelation
     */
    hostname: string;
    /**
     * The name of the server\'s provider.
     * @type {string}
     * @memberof ServerRelation
     */
    provider_name: string;
    /**
     * The human readable version of the provider\'s name
     * @type {string}
     * @memberof ServerRelation
     */
    provider_name_human_readable: string;
    /**
     * 
     * @type {CredentialRelation}
     * @memberof ServerRelation
     */
    credential: CredentialRelation | null;
    /**
     * The region in which the server is located
     * @type {string}
     * @memberof ServerRelation
     */
    region: string | null;
    /**
     * The human readable version of the region
     * @type {string}
     * @memberof ServerRelation
     */
    region_human_readable: string | null;
    /**
     * Public ipv4 address for server access
     * @type {string}
     * @memberof ServerRelation
     */
    ip_address: string;
    /**
     * The network port to which the SSH daemon is listening to SSH connections on the server
     * @type {number}
     * @memberof ServerRelation
     */
    ssh_port: number;
    /**
     * Tells if the server is active or not
     * @type {boolean}
     * @memberof ServerRelation
     */
    active: boolean;
    /**
     * 
     * @type {ActionStatus}
     * @memberof ServerRelation
     */
    status: ActionStatus;
    /**
     * 
     * @type {ActionRelationShallow}
     * @memberof ServerRelation
     */
    last_action: ActionRelationShallow | null;
    /**
     * The date and time when the record was created
     * @type {string}
     * @memberof ServerRelation
     */
    created_at: string;
    /**
     * The date and time when the record was last updated
     * @type {string}
     * @memberof ServerRelation
     */
    updated_at: string;
}

