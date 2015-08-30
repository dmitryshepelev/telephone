ALTER TABLE "main_app_userprofile" ADD COLUMN "secret_key" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_code" TYPE varchar(30);

ALTER TABLE "main_app_userprofile" DROP COLUMN "user_code" CASCADE;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_email" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_email" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_password" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_password" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "token" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "token" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "uid" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "uid" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "user_key" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" TYPE varchar(50);

ALTER TABLE "main_app_userprofile" DROP CONSTRAINT "main_app_userp_schema_id_4cddfcbff18e38b1_fk_main_app_schema_id";
ALTER TABLE "main_app_userprofile" DROP COLUMN "schema_id" CASCADE;
DROP TABLE "main_app_schema" CASCADE;