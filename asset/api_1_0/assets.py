# --*-- coding: utf-8 --*--
import json

import xlrd
from flask import request, jsonify
from flask_restful import Resource

from asset import api, db, logger
from asset.models.assets import AssetAssets, AssetType, AssetAgentType
from common.pagenate import get_page_items


class AssetsTypeListApi(Resource):
    def get(self):
        try:
            assets_types = db.session.query(AssetType).all()
            if not assets_types:
                return jsonify({"status": False, "desc": "资产类别数目为0"})
            asset_type_list = [assets_type._to_dict() for assets_type in assets_types]
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取资产类别失败"})
        return jsonify({"status": True, "assets_types": asset_type_list})


class AssetsAgentTypeListApi(Resource):
    def get(self):
        try:
            assets_agent_types = db.session.query(AssetAgentType).all()
            if not assets_agent_types:
                return jsonify({"status": False, "desc": "资产agent类别数目为0"})
            asset_agent_type_list = [assets_agent_type._to_dict() for assets_agent_type in assets_agent_types]
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取资产agent类别失败"})
        return jsonify({"status": True, "assets_agent_types": asset_agent_type_list})


class AssetsListApi(Resource):
    # def __init__(self):
    #     self.reqparse = reqparse.RequestParser()
    #     print self.reqparse.parse_args()
    #     self.reqparse.add_argument('serial_no', type=str, required=True,
    #                                help='No asset serial_no provided', location='json')
    #     super(AssetsListApi, self).__init__()

    def get(self):
        try:
            page, per_page, offset, search_msg = get_page_items()
            query = db.session.query(AssetAssets)
            assets = query.limit(per_page).offset(offset).all()
            total = query.count()
            if not assets:
                return jsonify({"status": False, "desc": "资产数目为0"})
            asset_list = [asset._to_dict() for asset in assets]
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取资产失败"})
        return jsonify({"status": True, "page": page, "per_page": per_page,
                        "total": total, "assets": asset_list})

    def post(self):
        try:
            data_json = request.get_json()
            asset_dict = json.loads(data_json)
            asset = AssetAssets._from_dict(asset_dict)

            db.session.add(asset)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "资产添加失败"})
        return jsonify({"status": True, "desc": "资产添加成功"})


class AssetsApi(Resource):
    def get(self, id):
        try:
            asset = db.session.query(AssetAssets).filter(AssetAssets.id == id).first()
            if not asset:
                return jsonify({"status": False, "desc": "无法查询到该资产"})
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "查询资产失败"})
        return jsonify({"status": True, "asset": asset._to_dict()})

    def put(self, id):
        try:
            asset = db.session.query(AssetAssets).filter(AssetAssets.id == id).first()
            if not asset:
                return jsonify({"status": False, "desc": "无法查询到该资产"})
            data_json = request.get_json()
            asset_dict = json.loads(data_json)
            asset.serial_no = asset_dict.get('serial_no')
            asset.name = asset_dict.get('name')
            asset.location = asset_dict.get('location')
            asset.owner = asset_dict.get('owner')
            asset.owner_contact = asset_dict.get('owner_contact')
            asset.type_id = asset_dict.get('type_id')
            asset.ip = asset_dict.get('ip')
            asset.agent_type_id = asset_dict.get('agent_type_id')
            asset.port = asset_dict.get('port')
            asset.network = asset_dict.get('network')
            asset.manufacturer = asset_dict.get('manufacturer')
            asset.describe = asset_dict.get('describe')
            db.session.add(asset)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "资产修改失败"})
        return jsonify({"status": True, "desc": "资产修改成功"})

    def delete(self, id):
        try:
            db.session.query(AssetAssets).filter(AssetAssets.id == id).delete()
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "资产删除失败"})
        return jsonify({"status": True, "desc": "资产删除成功"})


class AssetsFileApi(Resource):
    def post(self):
        try:
            files = request.files
            f = files['file']
            data = xlrd.open_workbook(filename=None, file_contents=f.read())
            sheet_data = data.sheets()[0]
            table = sheet_data._cell_values
            for row in table[1:]:
                asset = AssetAssets._from_excel_row(row)
                db.session.add(asset)
                db.session.flush()
            db.session.commit()

        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "资产导入失败"})
        return jsonify({"status": True, "desc": "资产导入成功"})


api.add_resource(AssetsTypeListApi, '/asset/api/v1.0/assets_types', endpoint='assets_types')
api.add_resource(AssetsAgentTypeListApi, '/asset/api/v1.0/assets_agent_types', endpoint='assets_agent_types')
api.add_resource(AssetsListApi, '/asset/api/v1.0/assets', endpoint='assets')
api.add_resource(AssetsApi, '/asset/api/v1.0/assets/<int:id>', endpoint='asset')
api.add_resource(AssetsFileApi, '/asset/api/v1.0/assets/file', endpoint='asset_file')
