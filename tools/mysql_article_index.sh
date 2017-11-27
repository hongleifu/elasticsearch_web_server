#!/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/java/bin/
export PATH;
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
bin=${DIR}/../bin
lib=${DIR}/../lib
id_begin=$1
id_end=$2
echo $id_begin
echo $id_end
echo '
{
    "type" : "jdbc",
    "autodiscover" : true,
    "jdbc" : {
        "useSSL" : false,
        "url" : "jdbc:mysql://localhost:3306/finance_one",
        "user" : "root",
        "password" : "123",
        "sql" : [{"statement":"select id as _id,title,content,content_html,url as url,uuid,intro_content,author,level,all_rank,final_level,publish_time_str,insert_time,tags,source_site_name,source_url,level_date,auto_abstract,content_sort,insert_date from article where id >= '${id_begin}' and id <= '${id_end}'"}],
        "index" : "finance",
        "type" : "article",
        "elasticsearch" : {
             "cluster" : "jinrongdao",
             "host" : "127.0.0.1",
             "port" : 9300
        }
    }
}
' | java \
    -cp "${lib}/*" \
    -Dlog4j.configurationFile=${bin}/log4j2.xml \
    org.xbib.tools.Runner \
    org.xbib.tools.JDBCImporter
