from http import HTTPStatus

STATUSES = {
    '200': HTTPStatus.OK,
    '302': HTTPStatus.FOUND,
    '404': HTTPStatus.NOT_FOUND,
}
